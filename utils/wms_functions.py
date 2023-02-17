import json
from rest_framework.views import APIView
from wmsconnectors.serializers import CompanyIntegrationSerializer, ConnectorLibrarySerializer
from wmsconnectors.utils.wms_facade import WMSFacade
from wmsconnectors.models import CompanyIntegration, ConnectorLibrary, SW_User
from django.http import HttpResponse, JsonResponse
from rest_framework.permissions import AllowAny
from wmsconnectors.utils.authenticate import authenticate


# @method_decorator(csrf_exempt, name='dispatch')
class WMSOrderData(APIView):
    authentication_classes = [AllowAny]

    def get(self, request):  
        username = self.request.query_params.get('username')
        user = SW_User.objects.get(username=username)
        company = user.company
        # we get connector of company by assuming that every company will have only one configuration
        wmsConnector = CompanyIntegration.objects.filter(company=company).first()
        if wmsConnector is not None:
            connector = WMSFacade.getConnectorInstace(wmsConnector.connector.connector_type)
            formatted_res = connector.get_order_data(wmsConnector)
            if formatted_res is None:
                return  HttpResponse(status=402)
            else:
                return JsonResponse({'new_template': formatted_res}, status=200)
        else:
            return  HttpResponse(status=402)

# @method_decorator(csrf_exempt, name='dispatch')
class ConnectorLibraryView(APIView):
    permission_classes = [AllowAny]

    def get_serialized(self):
        queryset = ConnectorLibrary.objects.all()
        serializer = ConnectorLibrarySerializer(queryset, many=True)
        data = serializer.data
        return data

    def get(self, request):  
        username = self.request.query_params.get('username')
        user = SW_User.objects.get(username=username)
        connectors = self.get_serialized()
        return JsonResponse({'connectors': list(connectors)}, status=200)

# @method_decorator(csrf_exempt, name='dispatch')
class CompanyIntegrationsView(APIView):
    permission_classes = [AllowAny]

    def get_serialized(self, company):
        # we are assuming that there will be only one integration per company
        integration = CompanyIntegration.objects.filter(company=company).first()
        if not integration:
            return None
        serializer = CompanyIntegrationSerializer(integration)
        data = serializer.data
        connector = ConnectorLibrary.objects.all().filter(id=data['connector']).first()
        company_config = data['connector_config']
        if not connector:
            return None
        if company_config:
            for structure in connector.connector_structure:
                # check if cat key exists in company
                structure_cat_key = structure['cat_key']
                if(structure_cat_key in company_config):
                    # if fields are not present in structure we directly add value inside structure
                    # else we add value inside every field
                    if 'fields' not in  structure:
                        structure['value'] = company_config[structure_cat_key]
                    else:
                        for field in structure['fields']:
                            # the value of company config's field key can be either a string or a dict
                            try:
                                if(type(company_config[structure_cat_key]) is dict):
                                    field['value'] = company_config[structure_cat_key][field['key']]
                                else:
                                    field['value'] = company_config[structure_cat_key]
                            except KeyError:
                                pass
        connector_serializer = ConnectorLibrarySerializer(connector)
        return connector_serializer.data

    def get(self, request):  
        username = self.request.query_params.get('username')
        user = SW_User.objects.get(username=username)
        company = user.company
        integrations = self.get_serialized(company=company)
        return JsonResponse(integrations, status=200, safe=False)

    def delete(self, request):  
        username = self.request.query_params.get('username')
        user = SW_User.objects.get(username=username)
        company = user.company
        # we are assuming that there will be only one integration per company
        integration = CompanyIntegration.objects.filter(company=company).first()
        if not integration:
            return None
        integration.delete()
        return HttpResponse(status=200)

# @method_decorator(csrf_exempt, name='dispatch')
class CompanyIntegrationConfig(APIView):
    permission_classes = [AllowAny]

    def post(self, request):  
        username = self.request.query_params.get('username')
        user = SW_User.objects.get(username=username)
        company = user.company
        requestData = json.loads(request.body)
        connectors = ConnectorLibrary.objects.filter(connector_type=requestData['connectorType'])
        if not connectors:
            return JsonResponse({'message': 'Connector does not exist'}, status=402)
        else:
            connector = connectors[0]
            companyIntegrations = CompanyIntegration.objects.filter(company=user.company)
            if not companyIntegrations:
                companyInegration = CompanyIntegration(company=user.company,connector_config=requestData['config'],connector=connector)
                companyInegration.save()
            else:
                for integration in companyIntegrations:
                    integration.connector_config = requestData['config']
                    integration.save()
            return HttpResponse(status=200)

    def delete(self, request):  
        username = self.request.query_params.get('username')
        user = SW_User.objects.get(username=username)
        company = user.company
        requestData = json.loads(request.body)
        connectors = ConnectorLibrary.objects.filter(connector_type=requestData['connectorType'])
        if not connectors:
            return JsonResponse({'message': 'Connector does not exist'}, status=402)
        else:
            connector = connectors[0]
            companyIntegrations = CompanyIntegration.objects.filter(company=user.company)
            if not companyIntegrations:
                return JsonResponse({'message': 'Company integration does not exist'}, status=402)
            else:
                for integration in companyIntegrations:
                    integration.connector_config = None
                    integration.save()
            return HttpResponse(status=200)

class User(APIView):
    permission_classes = [AllowAny]
    def get(self, request):  
        username = self.request.query_params.get('username')
        user = SW_User.objects.get(username=username)
        return JsonResponse({'userId': user.id},status=200)

