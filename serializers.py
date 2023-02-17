from wmsconnectors.models import ConnectorLibrary, CompanyIntegration, Company
from rest_framework import serializers

class CompanyIntegrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyIntegration
        fields = [
            'company',
            'connector',
            'connector_config',
        ] 
        lookup_field = 'id'

class ConnectorLibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = ConnectorLibrary
        fields = [
            'connector_name',
            'connector_type',
            'connector_network_type',
            'template_order',
            'template_inventory',
            'description',
            'base_url',
            'version',
            'logo',
            'connector_structure',
        ] 
        lookup_field = 'id'

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company 
        fields = [
                    'company_name',
                ]
        lookup_field = 'company_name'