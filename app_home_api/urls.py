from django.urls import path
from . import views
urlpatterns = [
    path('category/', views.category, name='categories_api'),  # List and create categories  

]
