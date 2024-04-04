from django_filters import FilterSet, ModelMultipleChoiceFilter, DateFilter
from django.forms import DateInput
from .models import Post, Category


class PostFilter(FilterSet):
    categories = ModelMultipleChoiceFilter(
        field_name="post_category",
        queryset=Category.objects.all(),
        label='Category',
        conjoined=True  # Осуществляем поиск сразу по нескольким категориям
    )

    date = DateFilter(
        field_name="post_time",
        label='Date',
        lookup_expr='lte',  # Используем оператор "меньше или равно" для поиска даты
        widget=DateInput(attrs={'type': 'date'})  # Используем виджет DateInput для отображения календаря
    )

    class Meta:
        model = Post
        fields = {
           'title': ['icontains'],
        }
