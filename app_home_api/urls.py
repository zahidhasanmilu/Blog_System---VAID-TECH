from django.urls import path,include    
from . import views
from rest_framework.routers import DefaultRouter




router = DefaultRouter()
router.register('categorie', views.CategoryViewSet, basename='api_categories')
router.register('tag', views.TagViewSet, basename='api_tag')
router.register('blog', views.BlogViewSet, basename='api_blog')


urlpatterns = [
    path('', include(router.urls)),
]