from import_export import resources
from .models import Purchase


class PurchaseResource(resources.ModelResource):
    class Meta:
        model = Purchase
