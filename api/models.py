from django.db import models


class InfoClient(models.Model):
    client_name = models.CharField(null=False, max_length=255, db_index=True, unique=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['client_name'], name='unique_client_name'),
        ]

    def __str__(self):
        return self.client_name

class ClientOrg(models.Model):
    client_name = models.ForeignKey(InfoClient, on_delete=models.PROTECT, null=False, related_name='client_name_clientorg')
    organisation = models.CharField(max_length=255, db_index=True, null=False)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.organisation

class OrganisationList(models.Model):
    client_name = models.ForeignKey(InfoClient, on_delete=models.PROTECT, null=False, related_name='name_client_orglist')
    name_org = models.ForeignKey('ClientOrg', on_delete=models.PROTECT, null=False, related_name='name_org_orglist')
    num_org = models.IntegerField(null=True, db_index=True)
    summ = models.IntegerField(null=True)
    date = models.DateField(null=True)
    service = models.CharField(max_length=255)
    fraud_score = models.FloatField(null=True)
    service_class = models.IntegerField(null=True)
    service_name = models.CharField(max_length=255, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["num_org", "name_org"], name='name of constraint'),
        ]

    def __str__(self):
        return self.name_org