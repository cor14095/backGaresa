from .models import Sales
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin


@admin.register(Sales)
class SalesAdmin(ImportExportModelAdmin):
    pass
