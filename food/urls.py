from django.contrib import admin
from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('api/food/', views.FoodList, name = 'FoodList'),
    path('api/food/<int:id>', views.FoodDetail, name = 'FoodDetail')
]

urlpatterns = format_suffix_patterns(urlpatterns)