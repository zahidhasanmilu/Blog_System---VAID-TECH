from django.urls import path,include    
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('categorie', views.CategoryViewSet, basename='category')
router.register('tag', views.TagViewSet, basename='tag')
router.register('blog', views.BlogViewSet, basename='blog')


urlpatterns = [
    path('', include(router.urls)),
]