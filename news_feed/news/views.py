from django.http import Http404
from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from .models import *
from .utils import q_search
from .forms import *


class ViewsTopicView(ListView):
    model = News
    template_name = 'news/news_topic.html'
    context_object_name = 'news_topic'
    slug_url_kwarg = 'topic_slug'
    paginate_by = 10
    ordering = ('-updated_date',)

    def get_queryset(self):
        topic_slug = self.kwargs.get(self.slug_url_kwarg)
        order_by = self.request.GET.get('order_by')
        query = self.request.GET.get('q')

        if topic_slug == 'all':
            news = super().get_queryset()
        elif query:
            news = q_search(query)
        else:                
            try:
                topic = NewsTopic.objects.get(slug=topic_slug)
                news = News.objects.filter(newstopic__slug=topic_slug)
                
                if not news.exists():
                    messages.warning(self.request, f"В коллекции '{topic.name}' пока нет новостей")
                    
            except NewsTopic.DoesNotExist:
                news = News.objects.none()
                messages.error(self.request, f"Коллекция не найдена")

        if order_by and order_by != 'default':
            news = news.order_by(order_by)
        return news

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        topic_slug = self.kwargs.get(self.slug_url_kwarg)
        
        if topic_slug != 'all':
            try:
                news_topic = NewsTopic.objects.get(slug=topic_slug)
                context["title"] = f'NewsFeed Новости  - {news_topic.name}'
            except NewsTopic.DoesNotExist:
                context["title"] = 'Новости'
        else:
            context["title"] = 'NewsFeed Новости — последние события России и мира сегодня, главные и актуальные новости'
        
        context["slug_url"] = topic_slug
        return context

class NewsView(DetailView):
    template_name = 'news/news.html'
    slug_url_kwarg = 'news_slug'
    context_object_name = 'news'

    def get_object(self, queryset = ...):
        return News.objects.get(slug=self.kwargs.get(self.slug_url_kwarg))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.object.title
        return context
    

class AddPageView(LoginRequiredMixin, CreateView):
    form_class = AddPostForm
    template_name = 'news/addpage.html'
    success_url = reverse_lazy('main:index')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.publication_date = timezone.now()
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление статьи'
        return context
    
