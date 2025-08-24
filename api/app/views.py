from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from .models import News, NewsTopic
from app.serializers import NewsSerializer, NewsTopicSerializer
from .permissions import *

class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    # pagination_class = PageNumberPagination
    permission_classes = (IsAdminOrReadOnly, )


class NewsTopicViewSet(viewsets.ModelViewSet):
    queryset = NewsTopic.objects.all()
    serializer_class = NewsTopicSerializer
    permission_classes = (IsAdminOrReadOnly, )



