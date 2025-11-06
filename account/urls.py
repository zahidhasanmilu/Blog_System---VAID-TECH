from django.urls import path
from .views import (
    User_ProfileView,
    activate_with_link,
    activate_with_otp,
    resend_verification,
    user_register,
    user_login,
    user_logout,
)

urlpatterns = [
    path("profile/<str:username>/", User_ProfileView, name="profile"),
    path("register/", user_register, name="register"),
    path("activate/<uuid:token>/", activate_with_link, name="activate_with_link"),
    path("verify-otp/", activate_with_otp, name="activate_with_otp"),
    path("resend-verification/", resend_verification, name="resend_verification"),
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="logout"),
]
