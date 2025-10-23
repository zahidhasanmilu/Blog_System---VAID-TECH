from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns
from django.conf import settings

from rest_framework.authtoken import views as drf_auth_views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', include('app_home.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),  
    path('account/', include('app_account.urls')),
    path('api/', include('app_home_api.urls')),  # API endpoints
    
    path('api-auth/', include('rest_framework.urls')),  # DRF login/logout views
    path('api-token-auth/', drf_auth_views.obtain_auth_token), # DRF token auth
    
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # JWT token obtain
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # JWT token refresh

]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Wrong Path Exception Handling
handler404 = 'app_home.views.custom_404'