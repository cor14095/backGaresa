from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import SalesViewSet

urlpatterns = [
    path('', SalesViewSet.as_view({'get': 'listcode'})),
    path('forecast/', SalesViewSet.as_view({'get': 'forecast'})),
]

urlpatterns = format_suffix_patterns(urlpatterns)