from django.shortcuts import render
from django.http import JsonResponse
from .serializers import CartSerializer
from .models import Cart
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response 

# Create your views here.
@api_view(['GET','POST'])
def CartList(request, format=None):
    #get all cart
    #serialize them
    #return json response
    if request.method == 'GET':
        carts = Cart.objects.all()
        serializer = CartSerializer(carts, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = CartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET','PUT','DELETE'])
def CartDetail(request, id, format=None):
    
    try:
        cart = Cart.objects.get(pk=id)
    except Cart.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = CartSerializer(cart)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = CartSerializer(cart, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)