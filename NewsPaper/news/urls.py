from django.urls import path
# Импортируем созданное нами представление
from .views import (
   NewsList, NewsDetail, PostCreate, PostUpdate, PostDelete
)


urlpatterns = [
   path('', NewsList.as_view()),
   path('<int:pk>', NewsDetail.as_view()),

   # Пути для Новостей
   path('news/create/', PostCreate.as_view(), name='news_create'),
   path('news/<int:pk>/update/', PostUpdate.as_view(), name='news_update'),
   path('news/<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),

   # Пути для Статей
   path('articles/create/', PostCreate.as_view(), name='articles_create'),
   path('articles/<int:pk>/update/', PostUpdate.as_view(), name='articles_update'),
   path('articles/<int:pk>/delete/', PostDelete.as_view(), name='articles_delete'),
]
