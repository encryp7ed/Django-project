from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from datetime import timedelta
from .models import Post, Category
from django.conf import settings


@shared_task
def send_news_notification(post_id):
    post = Post.objects.get(pk=post_id)
    subscribers = post.category.subscribers.all()

    if subscribers:
        subject = f"News update in the Category: {post.category.name}"
        text_content = post.content

        html_content = render_to_string(
            'appointment_created.html',
            {
                'post': post,
            }
        )

        from_email = settings.EMAIL_HOST_USER
        recipient_list = [subscriber.email for subscriber in subscribers]

        msg = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
        msg.attach_alternative(html_content, "text/html")
        msg.send()


@shared_task
def send_weekly_newsletter():
    # Получаем текущую дату и время
    end_date = timezone.now()
    start_date = end_date - timedelta(days=7)

    # Фильтруем новости за последние 7 дней
    news_last_7_days = Post.objects.filter(post_time__range=[start_date, end_date])

    # Находим новости за последнюю неделю
    if news_last_7_days.exists():
        # Создаем письмо
        subject = 'Weekly News Update'
        from_email = settings.EMAIL_HOST_USER,
        to = []

        # Получаем подписчиков для каждой категории
        categories = Category.objects.all()
        for category in categories:
            subscribers = category.subscribers.all()
            if subscribers.exists():
                for subscriber in subscribers:
                    to.append(subscriber.email)

        # Получаем список новостей за последнюю неделю
        html_content = render_to_string(
            'weekly_post.html',
            {'news_last_7_days': news_last_7_days}
        )

        # Отправляем письмо
        msg = EmailMultiAlternatives(subject, '', from_email, to)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
