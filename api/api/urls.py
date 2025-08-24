from django.urls import include, path, re_path
from django.contrib import admin


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('app.urls')),
    
    path('api/v1/drf-auth/', include('rest_framework.urls')),
    path('api/v1/auth/', include('djoser.urls')),
    path('api/v1/auth/', include('djoser.urls.jwt')),
]
