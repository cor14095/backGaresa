from import_export import resources
from .models import Sales


class ProductResource(resources.ModelResource):
    class Meta:
        model = Sales
