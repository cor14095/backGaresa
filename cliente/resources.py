from import_export import resources
from .models import Client


class ClientResource(resources.ModelResource):
    class Meta:
        model = Client
