from django.db import models


class Purchase(models.Model):
    """Database model for inventory in the system"""
    sociedad = models.CharField(max_length=50, null=True, blank=True)
    documento = models.CharField(max_length=50, null=True, blank=True)
    codigo_proveedor = models.CharField(max_length=25, null=True, blank=True)
    nombre_acreedor = models.CharField(max_length=255, null=True, blank=True)
    fecha_contabilizacion = models.DateField()
    codigo = models.CharField(max_length=25, null=True, blank=True)
    descripcion = models.CharField(max_length=255, null=True, blank=True)
    cantidad = models.FloatField(default=0.0, blank=True, null=True)
    precio = models.FloatField(default=0.0, blank=True, null=True)
    importe_comprado = models.FloatField(default=0.0, blank=True, null=True)

    def __str__(self):
        return self.codigo
