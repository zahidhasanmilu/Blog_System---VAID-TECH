from django.urls import path
from . import views
urlpatterns = [
    # path('category/', views.category, name='categories_api'),  # List and create categories  
    # path('tag/', views.tag, name='tags_api'),  # List and create tags

    # path('category/', views.CategoryListCreateMixinView.as_view(), name='categories_api'),  # List and create categories
    # path('category/<int:id>/', views.CategoryRetriveUpdateDeleteView.as_view(), name='category_detail_api'),  # Retrieve, update, delete a category
    
    path('category/', views.CategoryListCreateAPIView.as_view(), name='categories_api'),  # List and create categories
    path('category/<int:id>/', views.CategoryRetrieveUpdateDestroyAPIView.as_view(), name='category_detail_api'),  # Retrieve, update, delete a category
    
    path('tag/', views.TagListCreateAPIView.as_view(), name='tags_api'),  # List and create tags
    path('tag/<int:id>/', views.TagRetrieveUpdateDestroyAPIView.as_view(), name='tag_detail_api'),  # Retrieve, update, delete a tag
    
    path('blog/', views.BlogListCreateAPIView.as_view(), name='blogs_api'),  # List and create blogs
]   