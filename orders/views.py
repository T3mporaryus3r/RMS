from django.shortcuts import render
from .models import Order

def my_orders(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user)
    else:
        orders = Order.objects.filter(session_id=request.session.session_key)
    return render(request, "my_orders.html", {"orders": orders})
