from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.timezone import now

from news.models import *

@admin.register(NewsTopic)
class NewsTopicAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slug', 'display_id')
    list_display_links = ('name',)
    search_fields = ('name', 'slug')
    list_filter = ('name',)
    ordering = ('name',)
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'slug'),
            'description': 'Название коллекции и её URL-адрес'
        }),
    )
    
    def display_id(self, obj):
        return f"#{obj.id:03d}"
    display_id.short_description = 'ID'


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title_truncated', 'newstopic', 'publication_date_format', 
                   'user_username', 'image_preview', 'is_recent')
    list_display_links = ('title_truncated',)
    list_filter = ('newstopic', 'publication_date', 'user')
    search_fields = ('title', 'description', 'newstopic__name', 'user__username')
    readonly_fields = ('publication_date', 'updated_date')
    date_hierarchy = 'publication_date'
    list_per_page = 25
    actions = ['update_publication_date', 'duplicate_news']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'slug', 'description'),
            'description': 'Основные данные новости'
        }),
        ('Категория и медиа', {
            'fields': ('newstopic', 'image'),
            'description': 'Выберите коллекцию и загрузите изображение'
        }),
        ('Дополнительная информация', {
            'fields': ('user', 'publication_date', 'updated_date'),
            'classes': ('collapse',),
            'description': 'Технические данные'
        }),
    )
    
    def title_truncated(self, obj):
        return obj.title[:30] + '...' if len(obj.title) > 30 else obj.title
    title_truncated.short_description = 'Заголовок'
    
    def publication_date_format(self, obj):
        return obj.publication_date.strftime('%d.%m.%Y %H:%M')
    publication_date_format.short_description = 'Дата публикации'
    
    def user_username(self, obj):
        return obj.user.username if obj.user else '—'
    user_username.short_description = 'Автор'
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '📷 <a href="{}" target="_blank">Просмотр</a>',
                obj.image.url
            )
        return "—"
    image_preview.short_description = 'Изображение'
    
    def is_recent(self, obj):
        if (now() - obj.publication_date).days < 1:
            return "🆕 Сегодня"
        elif (now() - obj.publication_date).days < 7:
            return "🔥 Новое"
        return "—"
    is_recent.short_description = 'Статус'