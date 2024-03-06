from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        author = self.user.author
        # Получаем все статьи, опубликованные этим автором
        #  posts = Post.objects.filter(author=self.user.author)
        posts = author.post_set.all()

        # Получаем все комментарии этого автора
        comments = Comment.objects.filter(user=self.user)
        # Получаем все комментарии к статьям этого автора
        post_comments = Comment.objects.filter(post__in=posts)

        # Вычисляем рейтинг компонентов
        posts_rating = sum(post.rating for post in posts)
        comments_rating = sum(comment.rating for comment in comments)
        post_comments_rating = sum(comment.rating for comment in post_comments)

        # Обновляем общий рейтинг автора
        self.rating = posts_rating * 3 + comments_rating + post_comments_rating
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)


class Post(models.Model):
    NEWS = 'N'
    ARTICLE = 'A'
    POST_TYPES = [
        (NEWS, 'News'),
        (ARTICLE, 'Article')
    ]

    title = models.CharField(max_length=255)
    content = models.TextField()
    rating = models.IntegerField(default=0)

    categories = models.ManyToManyField(Category, through='PostCategory')
    post_time = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type = models.CharField(max_length=1, choices=POST_TYPES, default=ARTICLE)

    objects = models.Manager

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        # Получаем текст статьи или новости
        text = str(self.content)
        if len(text) > 124:
            # показываем только первые 124 символа
            return text[:124] + '...'
        else:
            return text

    def __str__(self):
        return self.title


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
