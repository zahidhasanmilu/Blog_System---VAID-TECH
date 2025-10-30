import time
from django.shortcuts import redirect, render, get_object_or_404
# Login MIXIN
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView

from blog.forms import BlogForm
# models
from .models import Blog, Category, Tag, BlogImage
from django.db.models import Q, Count

from django.core.paginator import Paginator


# Create your views here.

def custom_404(request, exception):
    return render(request, 'error404.html', status=404)

class HomeView(ListView):
    model = Blog
    template_name = 'index.html'  # specify your template
    context_object_name = 'blogs'  # the context variable in template
    paginate_by = 5  

    # Optional: use prefetch_related to optimize queries
    def get_queryset(self):
        return Blog.objects.prefetch_related('tags', 'blog_images').all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Aggregate: total number of blogs
        total_blogs = Blog.objects.aggregate(total=Count('id'))
        context['total_blogs'] = total_blogs['total']  # dictionary থেকে value
        return context



class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog/blog.html'  # specify your template
    context_object_name = 'blog'  # the context variable in template
    slug_field = 'slug'        # use slug field
    slug_url_kwarg = 'slug'    #  keyword argument

    def get_queryset(self):
        return Blog.objects.prefetch_related('tags', 'blog_images').all()
    
    
# class Tag_posts(ListView):
#     model = Blog
#     template_name = 'tag_posts.html'  # specify your template
#     context_object_name = 'blogs'  # the context variable in template

#     def get_queryset(self):
#         return Blog.objects.filter(tags__slug=self.kwargs['slug']).prefetch_related('tags', 'blog_images').all()


class TagPostsView(ListView):
    model = Blog
    template_name = 'blog/tag_blogs.html'
    context_object_name = 'tag_blogs'

    def get_queryset(self):
        # slug দিয়ে Tag বের করো
        self.tag = get_object_or_404(Tag, slug=self.kwargs['slug'])
        return self.tag.tag_blogs.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        return context


class CategoryBlogsView(ListView):
    model = Blog
    template_name = 'blog/category_blogs.html'
    context_object_name = 'category_blogs'

    def get_queryset(self):
        # filter category by slug
        start = time.time()
        
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        # return self.category.category_blogs.all()
        queryset = self.category.category_blogs.all()
        list(queryset)  # queryset evaluate
        duration = time.time() - start
        print(f"📊 Category query time: {duration:.4f} seconds")
        return queryset 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class SearchResultsView(ListView):
    model = Blog
    template_name = 'blog/search_results.html'
    context_object_name = 'blogs'

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        
        if query:
            return Blog.objects.filter(
                Q(title__icontains=query) |
                # Q(content__icontains=query) |
                Q(tags__title__icontains=query) |
                Q(category__title__icontains=query) |
                Q(author__username__icontains=query)
            ).distinct()
        else:
            return Blog.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        return context


def update_blog(request, id):
    blog = get_object_or_404(Blog, pk=id)
    if request.user != blog.author:
        return redirect('home')
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            blog = form.save()
            # Handle new image upload
            image = form.cleaned_data.get('image')
            if image:
                BlogImage.objects.create(blog=blog, image=image)
            return redirect('blog-detail', slug=blog.slug)
    else:
        form = BlogForm(instance=blog)

    context = {
        'form': form,
        'blog': blog
    }

    return render(request, 'blog/update_blog.html', context)


@login_required
def delete_blog(request, id):
    blog = get_object_or_404(Blog, pk=id)
    
    # Only author can delete
    if request.user != blog.author:
        return redirect('home')
    
    if request.method == 'POST':
        blog.delete()
        return redirect('profile', username=request.user.username)

    context = {
        'blog': blog
    }
    return render(request, 'blog/delete_blog.html', context)


from django.http import JsonResponse
from django.template.loader import render_to_string
from .models import Blog

def blog_search_ajax(request):
    query = request.GET.get('q', '')
    blogs = Blog.objects.select_related('author', 'category').prefetch_related('tags')

    if query:
        # filter by title OR category title OR tag title
        blogs = blogs.filter(
            Q(title__icontains=query) |
            Q(category__title__icontains=query) |
            Q(tags__title__icontains=query)
        ).distinct()[:10]  # limit results & distinct to avoid duplicates

    html = render_to_string('blog/includes/blog_list_items_dropdown.html', {'blogs': blogs})
    return JsonResponse({'html': html})

