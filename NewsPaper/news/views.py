from datetime import datetime, timedelta
from django.views.generic import ListView, DetailView
from .models import Post


class NewsList(ListView):
    model = Post
    # Вывод на страницу от "свежих" новостей к более старым
    ordering = 'post_time'
    template_name = 'news.html'
    context_object_name = 'news'

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
