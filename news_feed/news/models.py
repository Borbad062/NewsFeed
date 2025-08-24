from django.db import models
from django.utils import timezone
from users.models import User
from django.utils.text import slugify
from unidecode import unidecode


class NewsTopic(models.Model):
  name = models.CharField(
      max_length=150, 
      unique=True, 
      verbose_name='Название'
      )
  slug = models.CharField(
      max_length=200, 
      unique=True, 
      blank=True, 
      null=True, 
      verbose_name='URL'
      )

  class Meta:
    db_table = 'news_topic'
    verbose_name= 'Тема новостей'
    verbose_name_plural = 'Темы новостей'
    ordering = ['id']
  
  def __str__(self):
     return self.name


class News(models.Model):
  title = models.CharField(
      max_length=150, 
      unique=True, 
      verbose_name='Заголовок'
      )
  slug = models.SlugField(
      max_length=200, 
      unique=True,
      verbose_name='URL'
      )
  description = models.TextField(
      blank=True, 
      null=True, 
      verbose_name='Описание'
      )
  image = models.ImageField(
      upload_to='news_images', 
      blank=True, 
      null=True, 
      verbose_name='Изображение'
      )
  publication_date = models.DateTimeField(
      default=timezone.now,
      verbose_name='Дата публикации'
      )
  updated_date = models.DateTimeField(
      null=True, 
      blank=True,
      verbose_name='Дата обновления'
      )
  newstopic = models.ForeignKey(
      to=NewsTopic, 
      on_delete=models.CASCADE, 
      verbose_name='Темы'
      )
  user = models.ForeignKey(
      to=User, 
      on_delete=models.CASCADE, 
      blank=True, 
      null=True, 
      verbose_name='Пользователь'
      )
 
  class Meta:
        db_table = 'news'
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-updated_date']
  
  def __str__(self):
    return self.title
  
  def display_id(self):
        return f"{self.id:05}"
  
  def save(self, *args, **kwargs):
      if self.pk:
        self.updated_date = timezone.now()
      else:
          self.updated_date = None

      if not self.slug:
          base_slug = slugify(unidecode(self.title))
          self.slug = base_slug
          counter = 1
          while News.objects.filter(slug=self.slug).exists():
              self.slug = f"{base_slug}-{counter}"
              counter += 1
      super().save(*args, **kwargs)