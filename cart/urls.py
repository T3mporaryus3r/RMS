from django.contrib import admin
from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('api/cart/', views.CartList, name = 'CartList'),
    path('api/cart/<int:id>', views.CartDetail, name = 'CartDetail')
]

urlpatterns = format_suffix_patterns(urlpatterns)