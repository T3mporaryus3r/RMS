from django.contrib import admin
from django.urls import path
from website import views

urlpatterns = [
    path('', views.Home, name = 'Home'),
    path('Food',views.Food, name = 'Food'),
    path('Drinks',views.Drinks, name = 'Drinks'),
    path('Contact_Us', views.Contact_Us, name = 'Contact_Us'),
    path('About_Us', views.About_Us, name = 'About_Us'),
]