from abc import ABC, abstractmethod
from wmsconnectors.utils.wms_integration import import_template, import_template, wmsTransformData
from wmsconnectors.utils.wms_network import getNetworkInterface
from wmsconnectors.models import CompanyIntegration


class ConnectorInterface(ABC):
    # Get configurations
   @abstractmethod
   def init(self):
       pass
    # save configurations
   @abstractmethod
   def save(self):
       pass
   @abstractmethod
   def get_order_data(self):
       pass
   @abstractmethod
   def get_inventory_data(self):
       pass

class SAPConnector(ConnectorInterface):
    config = {}
    def init(self,wmsConnector):
        self.config = wmsConnector.connector_config
        pass
    def save():
        pass
    def get_order_data(self, wmsConnector: CompanyIntegration):
        self.init(wmsConnector)
        network_module = getNetworkInterface(wmsConnector.connector.connector_network_type)
        url = str(wmsConnector.connector.base_url) + str(wmsConnector.connector.version) + '/' + str(self.config['id'])
        res = network_module.get(url,headers=self.config['headers'])
        template = import_template(wmsConnector.connector.template_order)
        if res.status_code == 200:  
            return wmsTransformData(data = res.json(), template = template)
        else:
            return  None
    def get_inventory_data(self):
       self.init()
       pass

class SKUSavvyConnector(ConnectorInterface):
    config = {}
    warehouseId = ""
    def graphQlOrderQuery(self):
        return "{\"query\":\"query{\\r\\norders(originWarehouseId:\\\"" + self.warehouseId + "\\\"){\\r\\n \\r\\n   __typename\\r\\n  ... on CustomerOrder{\\r\\n  id\\r\\n  # friendlyId\\r\\n  createdAt\\r\\n  deliverAt\\r\\n  source\\r\\n  status\\r\\n  note\\r\\n  originWarehouseId\\r\\n  customerId\\r\\n  originWarehouse {\\r\\n    ...on Warehouse{ \\r\\n      id\\r\\n      createdAt\\r\\n      name\\r\\n      cycleCountConfig {\\r\\n        id\\r\\n        frequency\\r\\n        numOfBins\\r\\n        employees {\\r\\n        ... on WarehouseEmployee{\\r\\n          id\\r\\n          userId\\r\\n          user {\\r\\n            ...on PrivateUser{\\r\\n              id\\r\\n              createdAt\\r\\n              name\\r\\n              enabled\\r\\n              title\\r\\n              companyId\\r\\n              warehouseId\\r\\n   \\r\\n            }\\r\\n          }\\r\\n        }\\r\\n         \\r\\n         \\r\\n        }\\r\\n      }\\r\\n    }\\r\\n  }\\r\\n  shipments {\\r\\n    id\\r\\n    trackingNumber\\r\\n  }\\r\\n  quantities {\\r\\n        quantity : quantity\\r\\n        variant {\\r\\n          sku_id: sku\\r\\n            sku_price: price\\r\\n          productId  \\r\\n          product {\\r\\n            sku_category:type\\r\\n            sku_name:name\\r\\n            categories {\\r\\n              name\\r\\n            }\\r\\n          }    \\r\\n        }\\r\\n      }\\r\\n  customer {\\r\\n    id\\r\\n    name\\r\\n  }\\r\\n  location {\\r\\n    ... on Location{\\r\\n      id\\r\\n      createdAt\\r\\n      updatedAt\\r\\n      name\\r\\n      phone\\r\\n      email\\r\\n      address\\r\\n      address2\\r\\n      city\\r\\n      zip\\r\\n      storeId\\r\\n      countryId\\r\\n      stateId\\r\\n      shopifyId\\r\\n      customerId\\r\\n      companyId\\r\\n      warehouseId\\r\\n      customer {\\r\\n        ... on Customer{\\r\\n          id\\r\\n          createdAt\\r\\n          updatedAt\\r\\n          deliveryNote\\r\\n          deliveryRate\\r\\n          email\\r\\n          name\\r\\n          note\\r\\n          phone\\r\\n          wholesale\\r\\n          storeId\\r\\n          primaryLocation {\\r\\n            id\\r\\n          }\\r\\n          lastOrder {\\r\\n            ... on CustomerOrder{\\r\\n              id\\r\\n              friendlyId\\r\\n              createdAt\\r\\n              updatedAt\\r\\n              cancelledAt\\r\\n              deliverAt\\r\\n              test\\r\\n              source\\r\\n              status\\r\\n              tags\\r\\n              note\\r\\n              storeId\\r\\n              originWarehouseId\\r\\n              customerId\\r\\n              locationId\\r\\n       \\r\\n              shopifyId\\r\\n              originWarehouse {\\r\\n                ... on Warehouse{\\r\\n                  id\\r\\n                  createdAt\\r\\n                  updatedAt\\r\\n                  name\\r\\n                  prefix\\r\\n                  phone\\r\\n                  managerId\\r\\n                  companyId\\r\\n                  storeIds\\r\\n                  locationId\\r\\n                  returnLocation {\\r\\n                    id\\r\\n                  }\\r\\n                  cycleCountConfig {\\r\\n                    ... on CycleCountConfig{\\r\\n                      id\\r\\n                      frequency\\r\\n                      numOfBins\\r\\n                      employees {\\r\\n                        ... on WarehouseEmployee{\\r\\n                          id\\r\\nuserId\\r\\n                     \\r\\n                        }\\r\\n                      }\\r\\n                    }\\r\\n                  }\\r\\n                }\\r\\n              }\\r\\n            }\\r\\n          }\\r\\n        }\\r\\n      }\\r\\n    }\\r\\n  }\\r\\n  shippingLines {\\r\\n    ...on ShippingLine{\\r\\n      id\\r\\n      title\\r\\n      code\\r\\n      price\\r\\n    }\\r\\n  }\\r\\n}\\r\\n \\r\\n  __typename\\r\\n  ... on TransferOrder{\\r\\n    id\\r\\n    createdAt\\r\\n    updatedAt\\r\\n    cancelledAt\\r\\n    friendlyId\\r\\n    test\\r\\n    source\\r\\n    status\\r\\n    tags\\r\\n    note\\r\\n    originCompanyId\\r\\n    destinationCompanyId\\r\\n    originWarehouseId\\r\\n    quantities{\\r\\n      quantity\\r\\n    }\\r\\n    shopifyId\\r\\n    # destinationCompany {\\r\\n    #   id\\r\\n    # }\\r\\n    originWarehouse {\\r\\n      id\\r\\n    }\\r\\n    destinationWarehouse {\\r\\n      id\\r\\n      name\\r\\n    }\\r\\n    shipments {\\r\\n      id\\r\\n      createdAt\\r\\n      updatedAt\\r\\n      cancelledAt\\r\\n      deliveredAt\\r\\n      checkedInAt\\r\\n      estimatedDeliveryAt\\r\\n      fulfilledAt\\r\\n      shippedAt\\r\\n      status\\r\\n      orderId\\r\\n      originWarehouseId\\r\\n      packagingId\\r\\n      batchId\\r\\n      shipEngineId\\r\\n      shipEngineLabelId\\r\\n      shipEngineRateId\\r\\n      trackingNumber\\r\\n      priority\\r\\n      areaId\\r\\n      weight\\r\\n      weightUnit\\r\\n      fulfillmentId\\r\\n      fulfillmentOrderId\\r\\n      manually\\r\\n      split\\r\\n      barcodes {\\r\\n        id\\r\\n      }\\r\\n      rate {\\r\\n        id\\r\\n      }\\r\\n      tracking {\\r\\n        __typename\\r\\n        ... on ShipEngineTracking{\\r\\n          id\\r\\n          tracking_number\\r\\n          status_code\\r\\n          status_description\\r\\n          carrier_status_code\\r\\n          carrier_status_description\\r\\n          shipped_date\\r\\n          estimated_delivery_date\\r\\n          actual_delivery_date\\r\\n          exception_description\\r\\n          events {\\r\\n            city_locality\\r\\n            state_province\\r\\n            postal_code\\r\\n            country_code\\r\\n            company_name\\r\\n            signer\\r\\n            event_code\\r\\n          }\\r\\n        }\\r\\n      }\\r\\n      label {\\r\\n        id\\r\\n      }\\r\\n      quantities {\\r\\n        id\\r\\n      }\\r\\n     \\r\\n    }\\r\\n    quantities {\\r\\n      id\\r\\n    }\\r\\n  }\\r\\n \\r\\n}\\r\\n}\\r\\n\",\"variables\":{}}"
    def graphQlInventoryQuery(self):
        return ""
    def init(self,wmsConnector):
        self.config = wmsConnector.connector_config
        pass
    def save():
        pass
    def get_order_data(self, wmsConnector: CompanyIntegration):
        self.init(wmsConnector)
        network_module = getNetworkInterface(wmsConnector.connector.connector_network_type)
        url = str(wmsConnector.connector.base_url)
        self.warehouseId = self.config['WarehouseId']
        headers = {"X-Token": self.config['X-Token'], "Content-Type": "application/json"}
        res = network_module.post(url,headers=headers, payload=self.graphQlOrderQuery())
        template = import_template(wmsConnector.connector.template_order)
        if res.status_code == 200:  
            return wmsTransformData(data = res.json(), template = template)
        else:
            return  None
    def get_inventory_data(self, wmsConnector: CompanyIntegration):
        self.init(wmsConnector)
        network_module = getNetworkInterface(wmsConnector.connector.connector_network_type)
        url = str(wmsConnector.connector.base_url)
        self.warehouseId = self.config['WarehouseId']
        headers = {"X-Token": self.config['X-Token'], "Content-Type": "application/json"}
        res = network_module.post(url,headers=headers, payload=self.graphQlOrderQuery())
        template = import_template(wmsConnector.connector.template_order)
        if res.status_code == 200:  
            return wmsTransformData(data = res.json(), template = template)
        else:
            return  None
