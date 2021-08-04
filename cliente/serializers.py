from rest_framework import serializers
from .models import Client
from collections import OrderedDict


class ClientsDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'
    def to_representation(self, value):
        repr_dict = super(ClientsDetailSerializer, self).to_representation(value)
        return OrderedDict((k, v) for k, v in repr_dict.items()
                           if v not in [None, [], '', {}])
class ClientsGenericSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['codigo_cliente', 'nombre_cliente']
    def to_representation(self, value):
        repr_dict = super(ClientsGenericSerializer, self).to_representation(value)
        return OrderedDict((k, v) for k, v in repr_dict.items()
                           if v not in [None, [], '', {}])