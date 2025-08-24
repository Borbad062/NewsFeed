from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NewsViewSet, NewsTopicViewSet

router = DefaultRouter()
router.register(r'news', NewsViewSet)
router.register(r'topics', NewsTopicViewSet)

app_name = 'app'


urlpatterns = [
    path('v1/', include(router.urls)),
]
