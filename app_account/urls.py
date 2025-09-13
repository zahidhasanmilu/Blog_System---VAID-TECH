from django.urls import path
from .views import User_ProfileView

urlpatterns = [
    path('profile/<str:username>/', User_ProfileView, name='profile'),
]
