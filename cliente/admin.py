from .models import Client
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin


@admin.register(Client)
class ClientAdmin(ImportExportModelAdmin):
    pass
