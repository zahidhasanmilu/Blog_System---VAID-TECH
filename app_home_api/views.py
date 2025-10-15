from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view

from app_home.models import Blog, Category, Tag
from .serializers import CategorySerializer, TagSerializer

# Create your views here.

@api_view(['GET', 'POST'])
def category(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)