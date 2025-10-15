from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', include('app_home.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),  
    path('account/', include('app_account.urls')),
    path('api/', include('app_home_api.urls')),  # API endpoints
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Wrong Path Exception Handling
handler404 = 'app_home.views.custom_404'