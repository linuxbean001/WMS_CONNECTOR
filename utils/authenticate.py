from django.http import HttpResponse
from rest_framework.authtoken.models import Token
from django.conf import settings

def authenticate(request):
    try:
        token = Token.objects.all().get(key=request.auth)
        return token
    except Token.DoesNotExist:
        return None

