from rest_framework import serializers
from .models import Sales


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sales
        exclude = []
