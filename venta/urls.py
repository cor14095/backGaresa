from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import SalesViewSet

urlpatterns = [
    path('', SalesViewSet.as_view({'get': 'listcode'})),
    path('forecast/', SalesViewSet.as_view({'get': 'forecast'})),
    path('product_factor/', SalesViewSet.as_view({'get': 'product_factor'})),
]

urlpatterns = format_suffix_patterns(urlpatterns)