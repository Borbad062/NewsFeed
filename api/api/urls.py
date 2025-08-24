from django.urls import include, path, re_path

urlpatterns = [
    path('api/', include('app.urls')),
    
    path('api/v1/drf-auth/', include('rest_framework.urls')),
    path('api/v1/auth/', include('djoser.urls')),
    path('api/v1/auth/', include('djoser.urls.jwt')),
]
