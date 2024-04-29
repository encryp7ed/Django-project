from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone
from django.template.loader import render_to_string
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.conf import settings

from NewsPaper.news.models import Post, Category


# Отмечаем категории, на которые пользователь уже подписан
@login_required
def subscribe_category(request):
    categories = Category.objects.all()
    subscribed_categories = request.user.categories.all()
    context = {
        'categories': categories,
        'subscribed_categories': subscribed_categories,
    }
    return render(request, 'news_search.html', context)


# Подсписка на категории
@login_required
def subscribers(request, category_id):
    category = Category.objects.get(pk=category_id)
    request.user.subscribed_categories.add(category)
    return redirect('news_search.html')


# Рассылка новостей после их публикации
@receiver(post_save, sender=Post)
def notify_subscribers_post(sender, instance, created, **kwargs):
    if created:
        # Получаем список подписчиков для категории новости
        subscribers = instance.category.subscribers.all()

        # Формируем и отправляем письмо подписчикам
        if subscribers:
            # получаем наш html
            html_content = render_to_string(
                'appointment_created.html',
                {
                    'appointment': instance,
                    'link': f'{settings.SITE_URL}/news/{instance.pk}'
                }
            )

            msg = EmailMultiAlternatives(
                subject='',
                body='',
                from_email=settings.EMAIL_HOST_USER,
                to=[subscriber.email for subscriber in subscribers]
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()


# Ограничение на количество публикуемых новостей в день
@receiver(pre_save, sender=Post)
def limit_posts_per_day(sender, instance, **kwargs):
    # Проверяем, если запись создается и статус публикации
    if instance.pk is None and instance.status == 'published':
        # Получаем текущего пользователя, создающего запись
        user = instance.author

        # Получаем текущую дату и время
        today = timezone.now().date()

        # Получаем количество записей, опубликованных пользователем за сегодняшний день
        posts_today = Post.objects.filter(author=user, status='published', post_time__date=today).count()

        # Проверяем, сколько новостей пользователь уже опубликовал за сутки
        if posts_today >= 3:
            raise ValidationError("You cannot publish more than three news per day.")
