from django.contrib import admin
from .models import Product


#admin.site.register(Product)

from import_export.admin import ImportExportModelAdmin
from django.contrib import admin

@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    pass