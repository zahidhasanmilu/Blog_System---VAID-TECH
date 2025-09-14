from django.shortcuts import redirect, render, get_object_or_404


from .utils import logout_required
from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Forms
from .forms.login import LoginForm
from .forms.register import RegisterForm



# Models
from .models import Profile

#User
from django.contrib.auth import get_user_model
User = get_user_model()
from app_home.forms import BlogForm
from app_home.models import Blog, BlogImage



def User_ProfileView(request, username):
    profile_user = get_object_or_404(Profile, user__username=username)
    user_blogs = profile_user.user.user_blogs.all()

    form = None
    if request.user == profile_user.user:
        if request.method == 'POST':
            form = BlogForm(request.POST, request.FILES)
            if form.is_valid():
                blog = form.save(commit=False)
                blog.author = request.user
                blog.save()
                form.save_m2m()  # save tags

                # Handle single image extra field
                image = form.cleaned_data.get('image')
                if image:
                    BlogImage.objects.create(blog=blog, image=image)

                return redirect('profile', username=username)
        else:
            form = BlogForm()

    context = {
        'profile_user': profile_user,
        'user_blogs': user_blogs,
        'form': form
    }
    return render(request, 'app_account/profile.html', context)


@logout_required
def user_register(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data.get('firstName')
            last_name = form.cleaned_data.get('lastName')
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            # Create the user
            user = User.objects.create_user(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                username=username
                
            )

            messages.success(request, "Registration successful! You can now log in.")
            return redirect('login')
    else:
        form = RegisterForm()

    context = {
        "form": form
    }
    return render(request, "app_account/register.html", context)

@logout_required
def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            # form.valid হলে user অবশ্যই authenticate হয়েছে
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                messages.success(request, "Logged in successfully!")
                return redirect("home")
    else:
        form = LoginForm()

    context = {
        "form": form
    }
    return render(request, "app_account/login.html", context)


@login_required
def user_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect("login")
