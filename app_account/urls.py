from django.urls import path
from .views import User_ProfileView,blog_update

urlpatterns = [
    path('profile/<str:username>/', User_ProfileView, name='profile'),
    path('blog/<slug:slug>/update/',blog_update , name='blog-update'),
]
