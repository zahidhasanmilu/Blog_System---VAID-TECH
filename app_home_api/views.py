from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, GenericAPIView

from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework import viewsets

from app_home.models import Blog, Category, Tag
from .serializers import CategorySerializer, TagSerializer, BlogSerializer

from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, IsAdminUser

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

#pagination
from .paginations import CustomPagination
#filters
from .filters import BlogFilter

# Create your views here.
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    # filter_backends = [DjangoFilterBackend, SearchFilter] # Add not globally configured
  
    # filterset_fields = ['category', 'tags', 'title']
    filterset_class = BlogFilter
    
    # search_fields = ['title']
    search_fields = ['^title']
    
    ordering_fields = ['created_date', 'title']
    permission_classes = [IsAuthenticatedOrReadOnly] 
    pagination_class = CustomPagination
    
    def perform_create(self, serializer):
        serializer.save(author = self.request.user)

