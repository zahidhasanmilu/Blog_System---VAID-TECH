from django.urls import path
from .views import HomeView, BlogDetailView, TagPostsView, CategoryBlogsView, SearchResultsView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('blog/<slug:slug>/', BlogDetailView.as_view(), name='blog-detail'),
    path('tag/<slug:slug>/', TagPostsView.as_view(), name='tag-blogs'),
    path('category/<slug:slug>/', CategoryBlogsView.as_view(), name='category-blogs'),
    path('search/', SearchResultsView.as_view(), name='search'),
]
