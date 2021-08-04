from .models import Purchase
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin


@admin.register(Purchase)
class PurchaseAdmin(ImportExportModelAdmin):
    pass
