from .models import Blog, Category, Tag

def get_all_categories(request):
    categories = Category.objects.all()
    return {'categories': categories}

def get_all_tags(request):
    tags = Tag.objects.all()
    return {'tags': tags}

def get_recent_blogs(request):
    recent_blogs = Blog.objects.order_by('-created_date')[:5]
    return {'recent_blogs': recent_blogs}

