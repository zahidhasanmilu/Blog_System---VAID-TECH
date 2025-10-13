# import random
# from django.shortcuts import redirect
# from django.urls import reverse
# from django.contrib import messages
# from django.core.mail import send_mail
# from django.conf import settings
# from django.utils import timezone
# from datetime import timedelta

# from app_account.models import EmailVerification, CustomUser  # তোমার model নাম অনুযায়ী ঠিক করো


# class EmailVerificationMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         if request.user.is_authenticated:
#             if not getattr(request.user, "email_verified", True):
#                 allowed_paths = [
#                     reverse("logout"),
#                     reverse("verify_email", args=[request.user.id]),
#                 ]
#                 if request.path not in allowed_paths:
#                     # পুরনো OTP invalidate
#                     EmailVerification.objects.filter(user=request.user, is_used=False).update(is_used=True)

#                     # নতুন OTP তৈরি
#                     otp = str(random.randint(100000, 999999))
#                     EmailVerification.objects.create(user=request.user, otp=otp)

#                     # মেইল পাঠানো
#                     send_mail(
#                         "Verify Your Email",
#                         f"Your OTP is {otp}",
#                         settings.DEFAULT_FROM_EMAIL,
#                         [request.user.email],
#                     )

#                     messages.warning(request, "আপনার ইমেইল ভেরিফাই হয়নি। নতুন OTP পাঠানো হয়েছে।")
#                     return redirect("verify_email", user_id=request.user.id)

#         return self.get_response(request)

from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.conf import settings

User = get_user_model()

class ResendMailMiddleware:
    """
    Middleware:
    - Database এ ইউজার আছে কিনা চেক করে
    - যদি is_active=False হয় → resend_verification view এ রিডাইরেক্ট করে
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # শুধু POST বা GET request থেকে username/email ধরব
        username_or_email = (
            request.POST.get('email') or
            request.POST.get('username') or
            request.GET.get('email') or
            request.GET.get('username')
        )

        if username_or_email:
            try:
                user = User.objects.get(email=username_or_email)
                # যদি ইউজার inactive হয়
                if not user.is_active:
                    allowed_paths = [
                        reverse('resend_verification'),
                    ]
                    if request.path not in allowed_paths:
                        messages.info(request, f"{user.email} is not active. Please Check and verify your email.")
                        return redirect('resend_verification')
            except User.DoesNotExist:
                pass

        response = self.get_response(request)
        return response
