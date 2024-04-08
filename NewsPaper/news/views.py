from django.urls import reverse_lazy
from datetime import datetime, timedelta
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)

from django.contrib.auth.mixins import PermissionRequiredMixin

from .forms import PostForm
from .models import Post


class NewsList(ListView):
    model = Post
    ordering = 'post_time'  # Вывод на страницу от "свежих" новостей к более старым
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10  # Отображение не более 10 статей на странице

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # К словарю добавим популярную новость за последнюю неделю
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)

        # Фильтруем новости за последние 7 дней
        news_last_7_days = Post.objects.filter(post_time__range=[start_date, end_date])

        # Находим новость с наибольшим рейтингом
        if news_last_7_days.exists():
            top_news_of_week = news_last_7_days.order_by('-rating').first()
        else:
            top_news_of_week = None

        context['top_news_of_week'] = f"Новость недели: {top_news_of_week}"
        return context


class NewsDetail(DetailView):
    model = Post
    template_name = 'news_detail.html'
    context_object_name = 'news_detail'


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'news.add_post'
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        # Получаем инстанс модели, не сохраняя его в базу данных
        instance = form.save(commit=False)

        # Проверяем, откуда отправлен POST-запрос
        if self.request.path == '/news/create/':
            # Устанавливаем значение поля в "новость"
            instance.type = 'news'
        elif self.request.path == '/articles/create/':
            # Устанавливаем значение поля в "статья"
            instance.type = 'article'

        # Сохраняем объект модели с установленным значением поля
        return super().form_valid(form)


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'news.change_post'

    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'news.delete_post'

    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news_list')
