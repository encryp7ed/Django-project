from django.core.management.base import BaseCommand, CommandError
from NewsPaper.news.models import Post, Category


class Command(BaseCommand):
    help = 'Deletes all news from a specific category'
    # напоминать ли о миграциях. Если true — то будет напоминание о том, что не сделаны все миграции (если такие есть)
    requires_migrations_checks = True

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)

    def handle(self, *args, **options):
        self.stdout.readable()
        # спрашиваем пользователя, действительно ли он хочет удалить все статьи
        self.stdout.write(
            f'Do you really want to delete all news from {options["category"]} category? yes/no')
        answer = input()  # считываем подтверждение

        if answer == 'yes':  # в случае подтверждения действительно удаляем все товары
            category = Category.objects.get(name=options['category'])
            Post.objects.filter(category=category).delete()
            self.stdout.write(self.style.SUCCESS(f'Succesfully deleted all news from category {category.name}'))
            return

        # в случае неправильного подтверждения, говорим, что в доступе отказано
        self.stdout.write(
            self.style.ERROR('Access denied'))
