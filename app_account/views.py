from django.shortcuts import redirect, render, get_object_or_404

from app_home.forms import BlogForm
from app_home.models import BlogImage, Blog
from .models import Profile

from .utils import logout_required
from django.contrib.auth.decorators import login_required


@login_required
def User_ProfileView(request, username):
    profile_user = get_object_or_404(Profile, user__username=username)
    user_blogs = profile_user.user.user_blogs.all()  # Assuming a related_name='blogs' in Blog model's ForeignKey to CustomUser
    
    context = {
        'profile_user': profile_user,
        'user_blogs': user_blogs,
    }
    return render(request, 'app_account/profile.html', context)




@login_required
def blog_update(request, slug):
    blog = get_object_or_404(Blog, slug=slug, author=request.user)

    if request.method == "POST":
        form = BlogForm(request.POST, instance=blog)
        files = request.FILES.getlist('image')

        if form.is_valid():
            blog = form.save()

            # শুধু তখনই run করবে যখন files আছে
            if files:
                for f in files:
                    BlogImage.objects.create(blog=blog, image=f)

            return redirect(blog.get_absolute_url())

    else:
        form = BlogForm(instance=blog)

    images = blog.blog_images.all()  # পুরনো images

    return render(request, 'blog/blog_update_form.html', {
        'form': form,
        'blog': blog,
        'images': images
    })
