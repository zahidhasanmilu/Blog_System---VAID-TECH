from django.urls import path
from .views import (
    HomeView,
    BlogDetailView,
    TagPostsView,
    CategoryBlogsView,
    SearchResultsView,
    blog_search_ajax,
    update_blog,
    delete_blog,
)
from django.views.decorators.cache import cache_page

urlpatterns = [
    # path(
    #     "",
    #     cache_page(60 * 2)(HomeView.as_view()),  # <--- এই হলো সঠিক সিনট্যাক্স
    #     name="home",
    # ),
    path(
        "",
        HomeView.as_view(),
        name="home",
    ),
    path("blog/<slug:slug>/", BlogDetailView.as_view(), name="blog-detail"),
    path("tag/<slug:slug>/", TagPostsView.as_view(), name="tag-blogs"),
    path("category/<slug:slug>/", CategoryBlogsView.as_view(), name="category-blogs"),
    path("search-results/", SearchResultsView.as_view(), name="search-results"),
    # path('search/', blog_search, name='blog_search'),
    path("ajax/search/", blog_search_ajax, name="blog_search_ajax"),
    #  AJAX search
    path("update/<id>/", update_blog, name="update_blog"),
    path("delete/<int:id>/", delete_blog, name="delete_blog"),
]
