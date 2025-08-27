from django.contrib import admin
from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('api/drinks/', views.DrinksList, name = 'DrinksList'),
    path('api/drinks/<int:id>', views.DrinksList_detail, name = 'DrinksList_detail')
]

urlpatterns = format_suffix_patterns(urlpatterns)