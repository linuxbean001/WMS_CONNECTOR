from django.urls import path

from wmsconnectors.utils.wms_functions import *

from . import views

urlpatterns = [
    path('api/get_connector_order_data/', WMSOrderData.as_view()),
    path('api/get_connectors/', ConnectorLibraryView.as_view()),
    path('api/get_company_integrations/', CompanyIntegrationsView.as_view()),
    path('api/company_integration_config/', CompanyIntegrationConfig.as_view()),
    path('api/get_user_id/', User.as_view()),
]