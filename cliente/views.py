  
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
from .models import Client
from .serializers import ClientsGenericSerializer

class ClientViewSet(viewsets.ModelViewSet):

  @permission_classes([AllowAny, ]) 
  def list(self, request):
        queryset = Client.objects.all()
        serializer = ClientsGenericSerializer(queryset, many=True)
        return Response(serializer.data)