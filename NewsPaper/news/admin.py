from django.contrib import admin
from .models import Category, Post


# создаём новый класс для представления постов и категорий
class PostAdmin(admin.ModelAdmin):
    list_display = ('type', 'title', 'author', 'rating', 'categories')
    list_filter = ('type', 'title', 'author', 'rating', 'categories', 'post_time')
    search_fields = ('title', 'author', 'rating', 'category__name')


admin.site.register(Category)
admin.site.register(Post, PostAdmin)
