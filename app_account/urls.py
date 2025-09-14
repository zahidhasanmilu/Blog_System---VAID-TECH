from django.urls import path
from .views import User_ProfileView,user_register, user_login ,user_logout

urlpatterns = [
    path('profile/<str:username>/', User_ProfileView, name='profile'),
    
    path('register/', user_register, name='register'),    
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'), 
]
