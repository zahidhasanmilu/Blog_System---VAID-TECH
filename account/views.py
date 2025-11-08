from .tasks import send_verification_email_task
from django.utils import timezone
import uuid
from .models import CustomUser, EmailVerification
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

# --------

from blog.models import Blog, BlogImage
from blog.forms import BlogForm
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

# User
from django.db.models import Count
from django.contrib.auth import get_user_model

User = get_user_model()

import logging


# ------------------------------------------


def User_ProfileView(request, username):
    profile_user = get_object_or_404(Profile, user__username=username)
    user_blogs = profile_user.user.user_blogs.all()
    logger = logging.getLogger("create_blog")

    users_blog_count = (
        User.objects.filter(id=profile_user.user.id)
        .annotate(blog_count=Count("user_blogs"))
        .first()
        .blog_count
    )

    form = None
    if request.user == profile_user.user:
        if request.method == "POST":
            form = BlogForm(request.POST, request.FILES)
            if form.is_valid():
                blog = form.save(commit=False)
                blog.author = request.user
                blog.is_published = True
                blog.save()
                form.save_m2m()  # save tags

                # Handle single image extra field
                image = form.cleaned_data.get("image")
                if image:
                    BlogImage.objects.create(blog=blog, image=image)

                
                return redirect("profile", username=username)
            else:
                form = BlogForm(request.POST, request.FILES)
                logger.error("Blog form is not valid")
                print('Please fill all the fields')
        else:
            form = BlogForm()

    context = {
        "profile_user": profile_user,
        "user_blogs": user_blogs,
        "form": form,
        "users_blog_count": users_blog_count,
    }
    return render(request, "app_account/profile.html", context)


@logout_required
def user_register(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data.get("firstName")
            last_name = form.cleaned_data.get("lastName")
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")

            # Create the user
            user = User.objects.create_user(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                username=username,
            )

            # verification object create
            verification = EmailVerification.objects.create(user=user)
            verification.generate_otp()

            # send email
            send_verification_email(request, user)

            messages.success(
                request, "Registration successful! Please verify your email."
            )
            return redirect("activate_with_otp")
            # messages.success(request, "Registration successful! You can now log in.")
            # return redirect('login')
    else:
        form = RegisterForm()

    context = {"form": form}
    return render(request, "app_account/register.html", context)


# -------------------
# Send Verification Email
# -------------------
# def send_verification_email(request, user):
#     verification = user.verification

#     # ✅ Use reverse() for future-proof URL
#     link = request.build_absolute_uri(
#         reverse("activate_with_link", args=[verification.token])
#     )

#     subject = "Verify your email"
#     message = f"""
#     Hi {user.username},

#     Thanks for registering!

#     Please verify your email by clicking this link:
#     {link}

#     OR use this OTP: {verification.otp}

#     If you didn’t receive or your code expired, you can request a new one.
#     """
#     send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])


def send_verification_email(request, user):
    verification = user.verification

    link = request.build_absolute_uri(
        reverse("activate_with_link", args=[verification.token])
    )

    subject = "Verify your email"
    message = f"""
    Hi {user.username},

    Thanks for registering!

    Please verify your email by clicking this link:
    {link}

    OR use this OTP: {verification.otp}

    If you didn’t receive or your code expired, you can request a new one.
    """
    # Celery দিয়ে ব্যাকগ্রাউন্ডে ইমেইল পাঠানো
    send_verification_email_task.delay(subject, message, [user.email])


# -------------------
# Verify with Link
# -------------------


def activate_with_link(request, token):
    try:
        verification = EmailVerification.objects.get(token=token)
    except EmailVerification.DoesNotExist:
        messages.error(request, "Invalid verification link.")
        return render(request, "app_account/verification/activation_failed.html")

    # ✅ Expiry check
    if verification.expires_at and verification.expires_at < timezone.now():
        messages.error(request, "Verification link expired!")
        return render(request, "app_account/verification/activation_failed.html")

    # ✅ Activate user
    verification.is_verified = True
    verification.user.is_active = True
    verification.user.save()
    verification.save()

    messages.success(request, "Your email has been verified! You can now log in.")
    return redirect("login")


# -------------------
# Verify with OTP
# -------------------


def activate_with_otp(request):
    if request.method == "POST":
        otp = request.POST["otp"]
        try:
            verification = EmailVerification.objects.get(otp=otp)
        except EmailVerification.DoesNotExist:
            return render(
                request,
                "app_account/verification/verify_email.html",
                {"error": "Invalid OTP"},
            )

        if verification.expires_at and verification.expires_at < timezone.now():
            return render(
                request,
                "app_account/verification/verify_email.html",
                {"error": "OTP has expired. Please request a new one."},
            )

        verification.is_verified = True
        verification.user.is_active = True
        verification.user.save()
        verification.save()

        messages.success(request, "Your email has been verified! You can now log in.")
        return redirect("login")

    return render(request, "app_account/verification/verify_email.html")


# -------------------
# Resend Verification
# -------------------
def resend_verification(request):
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            user = CustomUser.objects.get(email=email)
            if user.is_active:
                messages.info(request, "This account is already verified.")
                return redirect("login")

            # new token + otp
            verification = user.verification
            verification.token = uuid.uuid4()
            verification.generate_otp()
            verification.save()

            send_verification_email(request, user)
            messages.success(request, "A new verification email has been sent!")
            return redirect("activate_with_otp")

        except CustomUser.DoesNotExist:
            messages.error(request, f"No account found with this email: {email}")
            return redirect("resend_verification")

    return render(request, "app_account/verification/resend_verification.html")


# ----------------------------User Login-------------------------------

"""
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


"""


@logout_required
def user_login(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                # এখানে success message দিলে user বুঝবে login complete,
                # কিন্তু middleware সাথে সাথেই redirect করবে resend_otp এ
                # তাই চাইলে message warning/success না-ও দিতে পারো
                return redirect("home")
    else:
        form = LoginForm()

    return render(request, "app_account/login.html", {"form": form})


@login_required
def user_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect("login")
