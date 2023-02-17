from django.db import models
from django.contrib.auth.models import User
from wmsconnectors.utils.enums import WMSConnectorNetworkType

class Company(models.Model):
    company_name = models.CharField("Company's Name", max_length=100)

class ConnectorLibrary(models.Model):
    connector_name = models.CharField("Connector Name", max_length=100,null=True, blank=True)
    connector_type = models.CharField("Connector Type", max_length=100,null=True, blank=True)
    connector_network_type = models.CharField(choices=WMSConnectorNetworkType.choices, null=True, default=None, max_length=20)
    template_order = models.FileField('Template - Order',null=True, blank=True)
    template_inventory = models.FileField('Template - Inventory', null=True, blank=True)
    description = models.CharField("Connector Description", max_length=100, null=True, blank=True)
    base_url = models.CharField("Connector Base Url", max_length=100,null=True, blank=True)
    version = models.CharField(max_length = 100, blank=True, null=True)
    logo = models.ImageField(upload_to="", null=True, blank=True)
    connector_structure = models.JSONField("Connector Structure", null=True, blank=True)

class CompanyIntegration(models.Model):
    company = models.ForeignKey(Company, null=True, on_delete=models.SET_NULL)
    connector = models.ForeignKey(ConnectorLibrary, null=True, on_delete=models.SET_NULL)
    connector_config = models.JSONField("Connector Configurations", null=True, blank=True)

class SW_User(User):
    company = models.ForeignKey(Company, related_name='members', null=True, on_delete=models.SET_NULL)

        