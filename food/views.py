from django.shortcuts import render
from django.http import JsonResponse
from .serializers import FoodSerializer
from .models import Food
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response 

# Create your views here.
@api_view(['GET','POST'])
def FoodList(request, format=None):
    #get all food
    #serialize them
    #return json response
    if request.method == 'GET':
        foods = Food.objects.all()
        serializer = FoodSerializer(foods, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = FoodSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET','PUT','DELETE'])
def FoodDetail(request, id, format=None):
    
    try:
        food = Food.objects.get(pk=id)
    except Food.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = FoodSerializer(food)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = FoodSerializer(food, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        food.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)