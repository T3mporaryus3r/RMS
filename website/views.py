from django.shortcuts import render, HttpResponse , get_object_or_404
from food.models import Food
from drinks.models import Drink
# from datetime import datetime
# from website.models import Contact
# from django.contrib import messages

# Create your views here.
def Home(request):
    return render(request, 'home.html')

def FoodListPage(request):
    foods = Food.objects.all()  # get all food 
    return render(request, "food.html", {"foods": foods})

def FoodDetailPage(request, id):
    food = get_object_or_404(Food, id=id)
    return render(request, "food_details.html", {"food": food})

def DrinksListPage(request):
    drinks = Drink.objects.all()  # get all food 
    return render(request, "drinks.html", {"drinks": drinks})

def DrinksList_detailPage(request, id):
    drink = get_object_or_404(Drink, id=id)
    return render(request, "drinks_details.html", {"drink": drink})

def Contact_Us(request):
    return render(request, 'contact_us.html')

def About_Us(request):
    return render(request, 'about_us.html')

def Cart(request):
    return render(request, 'cart.html')

