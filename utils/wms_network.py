import requests
from abc import ABC, abstractmethod
from wmsconnectors.utils.enums import WMSConnectorNetworkType

class NetworkInterface(ABC):
   @abstractmethod
   def get(self):
       pass
   def post(self):
       pass

def getNetworkInterface(networkType):
    match networkType:
        case WMSConnectorNetworkType.HTTPS:
            return HTTPSNetworkModule()

class HTTPSNetworkModule(NetworkInterface):
    def get(self, url, headers = None):
        r = requests.get(url, headers=headers)
        return r

    def post(self, url, headers = None, payload = None):
        r = requests.post(url, headers=headers,data=payload)
        return r