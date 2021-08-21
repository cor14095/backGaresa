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
    week = request.GET.get('week',None)
    year = request.GET.get('year',None)
    month = request.GET.get('month',None)
    day = request.GET.get('day',None)
    date = datetime.date.today()
    if year == None:
      year = date.year
    else:
      year = int(year)
    if week == None:
      week = date.isocalendar()[1]
    else:
      week = int(week)
    if month == None:
      month = date.month
    else:
      month = int(month)
    if day == None:
      day = date.day
    else:
      day = int(day)
    data = []
    start_year = 2015
    queryset = Sales.objects.all()
    selected_date = datetime.datetime(year,month,day)
    current_week = selected_date.strftime("%V")
    print(current_week,selected_date)
    if code != None:
      queryset = queryset.filter(codigo_cliente=code)
    if codeproduct != None:
      queryset = queryset.filter(codigo_producto=codeproduct)
    count = start_year
    while count <= year:
      d = '{0}-W{1}'.format(count,current_week)
      str_week = datetime.datetime.strptime(d + '-1', "%Y-W%W-%w")
      fin_week = str_week + datetime.timedelta(7)
      print(str_week,fin_week)
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
        "week": current_week, 
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
    fac_counter = 0
    factor_init = 0
    factor_fin = 0
    for forecast in data:
      week_data = forecast["data"]
      for x in range(7):
        dayIdx = x + 1
        day = next((item for item in week_data if item["day"] == dayIdx), None)
        dayData[x]['venta_neta'] += day['venta_neta'] if day else 0
        dayData[x]['cantidad_unidad'] += day['cantidad_unidad'] if day else 0
      if fac_counter == 5:
        factor_init = dayData[0]['venta_neta'] + \
            dayData[1]['venta_neta'] + \
            dayData[2]['venta_neta'] + \
            dayData[3]['venta_neta'] + \
            dayData[4]['venta_neta'] + \
            dayData[5]['venta_neta'] + dayData[6]['venta_neta']
      fac_counter += 1
    
    factor_fin = dayData[0]['venta_neta'] + \
        dayData[1]['venta_neta'] + \
        dayData[2]['venta_neta'] + \
        dayData[3]['venta_neta'] + \
        dayData[4]['venta_neta'] + \
        dayData[5]['venta_neta'] + dayData[6]['venta_neta']
        
    factor = factor_fin / factor_init
    #factor = 1.40
    print(factor, factor_init, factor_fin)
    data_length = len(dayData)
    avg_data = []
    unidades = 0
    for avg in dayData:
      avg_data.append({
        "venta_neta": avg['venta_neta']/data_length * factor,
        "cantidad_unidad" : avg['cantidad_unidad']/data_length * factor
      })
      unidades += avg['cantidad_unidad']/data_length * factor
    print(unidades)
    return Response(status = status.HTTP_200_OK,data=avg_data)

  @permission_classes([AllowAny, ]) 
  def product_factor(self, request):
    codeproduct = request.GET.get('product',None)
    year = request.GET.get('year',None)
    month = request.GET.get('month',None)
    day = request.GET.get('day',None)
    date = datetime.date.today()
    if year == None:
      year = date.year
    else:
      year = int(year)
    if month == None:
      month = date.month
    else:
      month = int(month)
    if day == None:
      day = date.day
    else:
      day = int(day)
    queryset = Sales.objects.all()
    selected_date = datetime.datetime(year,month,day)
    current_week = selected_date.strftime("%U")
    print(current_week)
    if codeproduct != None:
      queryset = queryset.filter(codigo_producto=codeproduct)
    count = 2015
    weekdata = []
    while count <= year:
      d = '{0}-W{1}'.format(count,current_week)
      str_week = datetime.datetime.strptime(d + '-1', "%Y-W%W-%w")
      fin_week = str_week + datetime.timedelta(6)
      print(str_week,fin_week)
      sales = (queryset
        .filter(fecha_documento__range=[str_week.strftime('%Y-%m-%d'),fin_week.strftime('%Y-%m-%d')])
        .annotate(year=ExtractYear('fecha_documento'))
        #.annotate(month=ExtractMonth('fecha_documento'))
        .annotate(week=ExtractWeek('fecha_documento'))
        .values('year', 'week',)
        .annotate(venta_neta=Sum('venta_neta'),cantidad_unidad=Sum('cantidad_unidad'))
      )
      if sales:
        for sale in sales:
          weekdata.append({
            "year": count,
            "week": current_week,
            "venta_neta": sale['venta_neta'],
            "cantidad_unidad": sale['cantidad_unidad']
          })
      else:
        weekdata.append({
            "year": count,
            "week": current_week,
            "venta_neta": 0,
            "cantidad_unidad": 0
        })
      count += 1
    return Response(status = status.HTTP_200_OK,data=weekdata)
