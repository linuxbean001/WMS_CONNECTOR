from django.db import models

class WMSConnectorNetworkType(models.TextChoices):
   HTTPS = "HTTPS"
   TCPIP = "TCP/IP"
   GRAPHQL="GRAPHQL"
   SDK="SDK"