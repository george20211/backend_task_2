from rest_framework import serializers
from .models import InfoClient, OrganisationList, ClientOrg
from django.db.models import Sum

class ClientListSerializer(serializers.ModelSerializer):
    count_org = serializers.SerializerMethodField()
    money_sum = serializers.SerializerMethodField()

    class Meta:
        model = InfoClient
        fields = ('client_name', 'count_org', 'money_sum')
    
    def get_count_org(self, obj):
        return len(OrganisationList.objects.filter(client_name=obj))

    def get_money_sum(self, obj):
        total_sum = OrganisationList.objects.filter(client_name=obj).aggregate(Sum('summ')).get('summ__sum')
        if type(total_sum) != int:
            return 0
        else: 
            return total_sum

class OrgListSerializer(serializers.ModelSerializer):
    client_name = serializers.SerializerMethodField()
    name_org = serializers.SerializerMethodField()

    class Meta:
        model = OrganisationList
        fields = '__all__'
    
    def get_client_name(self, obj):
        return str(obj.client_name)
    
    def get_name_org(self, obj):
        return str(obj.name_org)
