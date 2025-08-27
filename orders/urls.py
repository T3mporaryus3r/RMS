from django.contrib import admin
from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('api/orders/', views.OrdersList, name = 'OrdersList'),
    path('api/orders/<int:id>', views.OrdersDetail, name = 'OrdersDetail')
]

urlpatterns = format_suffix_patterns(urlpatterns)