from django.shortcuts import render, HttpResponse
# from datetime import datetime
# from website.models import Contact
# from django.contrib import messages

# Create your views here.
def Home(request):
    return render(request, 'home.html')

def Food(request):
    return render(request, 'food.html')

def Drinks(request):
    return render(request, 'drinks.html')

def Contact_Us(request):
    return render(request, 'contact_us.html')

def About_Us(request):
    return render(request, 'about_us.html')