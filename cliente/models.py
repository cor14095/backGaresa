from django.db import models

class Client(models.Model):
    """Database model for inventory in the system"""
    sociedad = models.CharField(max_length=50, null=True, blank=True)
    codigo_cliente = models.CharField(max_length=25, null=True, blank=True)
    nombre_cliente = models.CharField(max_length=255, null=True, blank=True)
    grupo = models.CharField(max_length=255, null=True, blank=True)
    fiscal_pais = models.CharField(max_length=25, null=True, blank=True)
    fiscal_direccion = models.CharField(max_length=255, null=True, blank=True)
    fiscal_ciudad = models.CharField(max_length=50, null=True, blank=True)
    fiscal_departamento = models.CharField(
        max_length=50, null=True, blank=True)
    fiscal_municipio = models.CharField(max_length=50, null=True, blank=True)
    entrega_pais = models.CharField(max_length=10, null=True, blank=True)
    entrega_direccion = models.CharField(max_length=255, null=True, blank=True)
    entrega_ciudad = models.CharField(max_length=50, null=True, blank=True)
    entrega_departamento = models.CharField(max_length=50, null=True, blank=True)
    entrega_municipio = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(max_length=25, null=True, blank=True)

    def __str__(self):
        return self.codigo_cliente
