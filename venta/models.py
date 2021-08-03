from django.db import models


class Sales(models.Model):
    """Database model for inventory in the system"""
    sociedad = models.CharField(max_length=50, null=True, blank=True)
    tipo_documento = models.CharField(max_length=50, null=True, blank=True)
    numero_documento = models.IntegerField(default=0)
    vendedor = models.IntegerField(default=0)
    codigo_cliente = models.CharField(max_length=50, null=True, blank=True)
    nombre_cliente = models.CharField(max_length=255, null=True, blank=True)
    fecha_documento = models.DateField()
    codigo_producto = models.CharField(max_length=50, null=True, blank=True)
    producto = models.CharField(max_length=255, null=True, blank=True)
    cantidad_unidad = models.FloatField(default=0.0, blank=True, null=True)
    cantidad_inventario = models.FloatField(default=0.0, blank=True, null=True)
    venta_bruta = models.FloatField(default=0.0, blank=True, null=True)
    venta_neta = models.FloatField(default=0.0, blank=True, null=True)
    costo = models.FloatField(default=0.0, blank=True, null=True)

    def __str__(self):
        return self.nombre_cliente
