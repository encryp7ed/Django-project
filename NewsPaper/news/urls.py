from django.urls import path
from django.views.decorators.cache import cache_page
from .views import (
   NewsList, NewsDetail, PostCreate, PostUpdate, PostDelete
)


urlpatterns = [
   path('', cache_page(60*1)(NewsList.as_view())),
   path('<int:pk>', cache_page(60*5)(NewsDetail.as_view())),

   # Пути для Новостей
   path('news/create/', PostCreate.as_view(), name='news_create'),
   path('news/<int:pk>/update/', PostUpdate.as_view(), name='news_update'),
   path('news/<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),

   # Пути для Статей
   path('articles/create/', PostCreate.as_view(), name='articles_create'),
   path('articles/<int:pk>/update/', PostUpdate.as_view(), name='articles_update'),
   path('articles/<int:pk>/delete/', PostDelete.as_view(), name='articles_delete'),
]
