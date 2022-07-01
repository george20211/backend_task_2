from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import InfoClient, OrganisationList, ClientOrg
from .serializer import ClientListSerializer, OrgListSerializer
from django.core.exceptions import ObjectDoesNotExist
from pandas import read_excel
import openpyxl
import random
import datetime as dt


class ClientListViewSet(viewsets.ViewSet):

    def list(self, request):
        queryset = InfoClient.objects.all()
        serializer = ClientListSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrgListViewSet(viewsets.ViewSet):

    def list(self, request):
        queryset = OrganisationList.objects.all()
        obj = request._request.GET
        if len(obj) > 0:
            if 'client' in obj:
                client = obj.get('client')
                try:
                    owner = InfoClient.objects.get(client_name=client).id
                except ObjectDoesNotExist:
                    msg = 'Имя клиента не найдено'
                    return Response(msg, status=status.HTTP_200_OK)
                queryset = queryset.filter(client_name=owner)
            if 'org' in obj:
                org = obj.get('org')
                try:
                    org_id = ClientOrg.objects.get(organisation=org).id
                except ObjectDoesNotExist:
                    msg = 'Организация не найдена'
                    return Response(msg, status=status.HTTP_200_OK)
                queryset = queryset.filter(name_org=org_id)
        serializer = OrgListSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DownloadViewSet(viewsets.ViewSet):

    @staticmethod
    def fraud_detector(unknown_string: str) -> float:
        return random.randint(float(0), float(1))

    @staticmethod
    def service_classifier(unknown_string: str) -> dict:
        data = {
            1: 'консультация',
            2: 'лечение',
            3: 'стационар',
            4: 'диагностика',
            5: 'лаборатория',
        }
        random_int = random.randint(1, 5)
        return {'service_class': int(random_int),
                'service_name': str(data[random_int])}

    def get_filename(self, request, format=None):
        for file in request.FILES.getlist('file'):
            if str(file) == 'client_org.xlsx':
                queryset_client = InfoClient.objects.all()
                data_client_list = []
                file = openpyxl.open(file)
                sheet = file.active
                row = 2
                while type(sheet[row][0].value) == str:
                    client = sheet[row][0].value
                    if queryset_client.filter(client_name=client).exists():
                        print("Клиент с таким именем уже есть")
                    else:
                        data_client_list += [InfoClient(client_name=client)]
                    row += 1
                InfoClient.objects.bulk_create(data_client_list)
                data_org_client = []
                sheet2 = file.worksheets[1]
                queryset_client = InfoClient.objects.all()
                queryset_client_org = ClientOrg.objects.all()
                for cl_name, name, address in sheet2['A2':f'C{sheet2.max_column+1}']:
                    client_name = queryset_client.get(client_name=str(cl_name.value))
                    if queryset_client_org.filter(client_name=client_name,
                                                  organisation=str(name.value)).exists():
                        print('Уже есть')
                        pass
                    else:
                        name_org = str(name.value)
                        address=str(address.value)
                        data_client_list = []
                        data_org_client += [ClientOrg(client_name=client_name,
                                                      organisation=name_org,
                                                      address=address)]
                ClientOrg.objects.bulk_create(data_org_client)
        for file in request.FILES.getlist('file'):
            if str(file) == 'bills.xlsx':
                df = read_excel(file)
                data = []
                queryset_client = InfoClient.objects.all()
                queryset_org = ClientOrg.objects.all()
                queryset_org_all = OrganisationList.objects.all()
                for row in df.itertuples():
                    client_name = queryset_client.get(client_name=str(row[1]))
                    name_org = queryset_org.get(organisation=str(row[2]))
                    num_org = int(row[3])
                    summ = float(row[4])
                    date = dt.datetime.strptime(str(row[5]), "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
                    service = str(row[6])
                    fraud_score = self.fraud_detector('что-то отсылаем в детектор')
                    result_classifer = self.service_classifier(service)
                    service_class = result_classifer.get('service_class')
                    service_name = result_classifer.get('service_name')
                    if queryset_org_all.filter(name_org=name_org, num_org=num_org).exists():
                        print(f'запись с {num_org} номером для организации {name_org} уже есть')
                        pass
                    else:
                        data += [OrganisationList(client_name=client_name,
                                                  name_org=name_org,
                                                  num_org=num_org,
                                                  summ=summ,
                                                  date=date,
                                                  service=service,
                                                  fraud_score=fraud_score,
                                                  service_class=service_class,
                                                  service_name=service_name
                                                  )]
                OrganisationList.objects.bulk_create(data)
        msg = 'Валидные файлы были обработаны'
        return Response(msg, status=status.HTTP_200_OK)
