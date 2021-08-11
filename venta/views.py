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
from .serializers import SalesGenericSerializer
from django.db.models import Sum,Avg
import datetime
from django.db.models.functions import ExtractWeek, ExtractYear,ExtractWeekDay,ExtractMonth

class SalesViewSet(viewsets.ModelViewSet):
  @permission_classes([AllowAny, ]) 
  def listcode(self, request):
      code = request.GET.get('client',None)
      codeproduct = request.GET.get('product',None)
      month = request.GET.get('month',None)
      year = request.GET.get('year',None)
      queryset = Sales.objects.all()
      if code != None:
        queryset = queryset.filter(codigo_cliente=code)
      if codeproduct != None:
        queryset = queryset.filter(codigo_producto=codeproduct)
      if month != None and year != None:
        queryset = queryset.filter(fecha_documento__year__gte=year,
          fecha_documento__month__gte=month,
          fecha_documento__year__lte=year,
          fecha_documento__month__lte=month,
        )
      result = queryset.values('fecha_documento').order_by('fecha_documento').annotate(venta_neta=Sum('venta_neta'),cantidad_unidad=Sum('cantidad_unidad'))
      serializer = SalesGenericSerializer(result, many=True)
      return Response(serializer.data)

  @action(detail=False, methods=['GET'], url_path = 'forecast')
  def forecast(self, request):
    code = request.GET.get('client',None)
    codeproduct = request.GET.get('product',None)
    date = datetime.date.today()
    year = date.year
    start_year = year - 6
    week = date.isocalendar()[1]
    data = []
    queryset = Sales.objects.all()
    if code != None:
      queryset = queryset.filter(codigo_cliente=code)
    if codeproduct != None:
      queryset = queryset.filter(codigo_producto=codeproduct)
    count = start_year
    while count <= year:
      d = '{0}-W{1}'.format(count,week)
      str_week = datetime.datetime.strptime(d + '-1', "%Y-W%W-%w")
      fin_week = str_week + datetime.timedelta(7)
      sales = (queryset
        .filter(fecha_documento__range=[str_week.strftime('%Y-%m-%d'),fin_week.strftime('%Y-%m-%d')])
        .annotate(year=ExtractYear('fecha_documento'))
        .annotate(month=ExtractMonth('fecha_documento'))
        .annotate(week=ExtractWeek('fecha_documento'))
        .annotate(day=ExtractWeekDay('fecha_documento'))
        .values('year', 'month', 'week', 'day')
        .annotate(venta_neta=Sum('venta_neta'),cantidad_unidad=Sum('cantidad_unidad'))
      )
      weekdata = []
      if sales:
        for sale in sales:
          weekdata.append(sale)
        
      data.append({
        "year": count,
        "week": week, 
        "data": weekdata
      })
      count += 1
    
    dayData = [
      {
        'venta_neta': 0,
        'cantidad_unidad': 0,
      },
      {
        'venta_neta': 0,
        'cantidad_unidad': 0,
      },
      {
        'venta_neta': 0,
        'cantidad_unidad': 0,
      },
      {
        'venta_neta': 0,
        'cantidad_unidad': 0,
      },
      {
        'venta_neta': 0,
        'cantidad_unidad': 0,
      },
      {
        'venta_neta': 0,
        'cantidad_unidad': 0,
      },
      {
        'venta_neta': 0,
        'cantidad_unidad': 0,
      }
    ]
    for forecast in data:
      week_data = forecast["data"]
      for x in range(7):
        dayIdx = x + 1
        day = next((item for item in week_data if item["day"] == dayIdx), None)
        print(day)
        dayData[x]['venta_neta'] += day['venta_neta'] if day else 0
        dayData[x]['cantidad_unidad'] += day['cantidad_unidad'] if day else 0
    data_length = len(dayData)
    avg_data = []
    for avg in dayData:
      avg_data.append({
        "venta_neta": avg['venta_neta']/data_length,
        "cantidad_unidad" : avg['cantidad_unidad']/data_length
      })
    
    return Response(status = status.HTTP_200_OK,data=avg_data)