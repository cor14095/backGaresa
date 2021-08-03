from .models import Product
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin

@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    pass