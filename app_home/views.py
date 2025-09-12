from django.shortcuts import render
# Login MIXIN
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
#models
from .models import Blog, Category, Tag, BlogImage


# Create your views here.
class HomeView(ListView):
    model = Blog
    template_name = 'index.html'  # specify your template
    context_object_name = 'blogs'  # the context variable in template

    # Optional: use prefetch_related to optimize queries
    def get_queryset(self):
        return Blog.objects.prefetch_related('tags', 'blog_images').all()