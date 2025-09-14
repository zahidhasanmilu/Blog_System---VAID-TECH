from django.shortcuts import redirect, render, get_object_or_404
# Login MIXIN
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView

from app_home.forms import BlogForm
# models
from .models import Blog, Category, Tag, BlogImage
from django.db.models import Q


# Create your views here.
class HomeView(ListView):
    model = Blog
    template_name = 'index.html'  # specify your template
    context_object_name = 'blogs'  # the context variable in template

    # Optional: use prefetch_related to optimize queries
    def get_queryset(self):
        return Blog.objects.prefetch_related('tags', 'blog_images').all()


class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog/blog.html'  # specify your template
    context_object_name = 'blog'  # the context variable in template
    slug_field = 'slug'        # model এর কোন field দিয়ে খুঁজবে
    slug_url_kwarg = 'slug'    # URL এর keyword argument

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
        # slug দিয়ে Category বের করো
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return self.category.category_blogs.all()

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
                Q(content__icontains=query) |
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
