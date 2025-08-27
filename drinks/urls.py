from django.contrib import admin
from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('api/drinks/', views.DrinkList, name = 'DrinkList'),
    path('api/drinks/<int:id>', views.DrinkList_detail, name = 'DrinkList_detail')
]

urlpatterns = format_suffix_patterns(urlpatterns)