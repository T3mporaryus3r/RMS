from django.contrib import admin
from django.urls import path, include
from website import views

urlpatterns = [
    path("", views.Home, name="Home"),
    path("Food", views.FoodListPage, name="FoodListPage"),
    path("Food/<int:id>", views.FoodDetailPage, name="FoodDetailPage"),
    path("Drinks", views.DrinksListPage, name="DrinksListPage"),
    path("Drinks/<int:id>", views.DrinksList_detailPage, name="DrinksList_detailPage"),
    path("Contact_Us", views.Contact_Us, name="Contact_Us"),
    path("About_Us", views.About_Us, name="About_Us"),
    path("payments/", include('payments.urls')),
    path("cart/", include("cart.urls")),
    path("orders/", include("orders.urls")),
]
