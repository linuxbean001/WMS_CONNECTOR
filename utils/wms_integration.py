import pyjq
from django.core.files import File

def import_template(obj: File):
    file = obj.open('r')
    template = file.read()
    file.close()
    return template

def wmsTransformData(data, template):
        formatted_modify = pyjq.all(template, data)
        return formatted_modify