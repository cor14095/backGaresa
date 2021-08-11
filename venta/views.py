  
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import serializers, status, viewsets
from rest_framework.generics import ListAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from .models import Sales
from .serializers import SalesGenericSerializer, SalesDetailSerializer


class SalesViewSet(viewsets.ModelViewSet):



  @permission_classes([AllowAny, ]) 
  def listcode(self, request):
      code = request.GET.get('client',None)
      codeproduct = request.GET.get('product',None)
      if code == None and codeproduct == None:
        queryset = Sales.objects.all()
      if code != None:
        queryset = Sales.objects.all().filter(codigo_cliente=code)
      if codeproduct != None:
        queryset = Sales.objects.all().filter(codigo_producto=codeproduct)
      if code != None and codeproduct != None:
        queryset = Sales.objects.all().filter(codigo_producto=codeproduct,codigo_cliente = code)
      serializer = SalesGenericSerializer(queryset, many=True)
      return Response(serializer.data)