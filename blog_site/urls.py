from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns
from django.conf import settings

from rest_framework.authtoken import views as drf_auth_views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


# ------------- for Swagger
from django.urls import path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="My API",
        default_version="v1",
        description="Test API documentation",
        contact=openapi.Contact(email="your@email.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
# ----------swagger-----------

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("blog.urls")),
    path("ckeditor/", include("ckeditor_uploader.urls")),
    path("account/", include("account.urls")),
    path("api/", include("blog_api.urls")),  # API endpoints
    path("api-auth/", include("rest_framework.urls")),  # DRF login/logout views
    path("api-token-auth/", drf_auth_views.obtain_auth_token),  # DRF token auth
    path(
        "api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"
    ),  # JWT token obtain
    path(
        "api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"
    ),  # JWT token refresh
    # ----swagger -------------
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    # -----swagger ---------------
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Wrong Path Exception Handling
handler404 = "blog.views.custom_404"
