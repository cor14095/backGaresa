from rest_framework import serializers
from .models import Sales
from collections import OrderedDict
from cliente.serializers import ClientsGenericSerializer

class SalesDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sales
        fields = '__all__'
    def to_representation(self, value):
        repr_dict = super(SalesDetailSerializer, self).to_representation(value)
        return OrderedDict((k, v) for k, v in repr_dict.items()
                           if v not in [None, [], '', {}])
class SalesGenericSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sales
        fields = ['id','codigo_cliente','nombre_cliente', 'codigo_producto','cantidad_unidad','venta_neta']
    def to_representation(self, value):
        repr_dict = super(SalesGenericSerializer, self).to_representation(value)
        return OrderedDict((k, v) for k, v in repr_dict.items()
                           if v not in [None, [], '', {}])