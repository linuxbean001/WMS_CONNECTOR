from wmsconnectors.utils.wms_connectors import  SAPConnector, SKUSavvyConnector

class WMSFacade:

    def getConnectorInstace(wmsConnector):
        match wmsConnector:
            case "SAP":
                return SAPConnector()
            case "SKUSavvy":
                return SKUSavvyConnector()



