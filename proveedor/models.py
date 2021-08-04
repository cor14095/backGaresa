from django.db import models


class Providers(models.Model):
    """Database model for inventory in the system"""
    sociedad = models.CharField(max_length=50, null=True, blank=True)
    codigo = models.CharField(max_length=25, null=True, blank=True)
    descripcion = models.CharField(max_length=255, null=True, blank=True)
    grupo = models.CharField(max_length=255, null=True, blank=True)
    costo = models.FloatField(default=0.0, blank=True, null=True)
    fecha_cierre = models.DateField()
    cantidad_cierre = models.FloatField(default=0.0, blank=True, null=True)
    stock = models.FloatField(default=0.0, blank=True, null=True)
    pedido = models.IntegerField(default=0)

    def __str__(self):
        return self.codigo
