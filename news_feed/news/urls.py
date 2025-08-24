from django.urls import path, include
from .views import *

app_name='news'

urlpatterns = [
    path('addpage/', AddPageView.as_view(), name='addpage'),
    path('search/', ViewsTopicView.as_view(), name='search'),
    path('<slug:topic_slug>/', ViewsTopicView.as_view(), name='index'),
    path('item/<slug:news_slug>/', NewsView.as_view(), name='news'),
]