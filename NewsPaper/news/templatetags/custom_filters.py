from django import template
import re


register = template.Library()


@register.filter()
def censorship(value):
    # Создаем ограничение на тип входных данных
    if not isinstance(value, str):
        raise TypeError()

    # Создаем список запрещенных слов
    censored_words = ['bad_word1', 'bad_word2', 'bad_word3']
    for word in censored_words:
        # создаем регулярное выражение из нецензурных слов
        # re.IGNORECASE для игнорирования регистра
        pattern = re.compile(re.escape(word), flags=re.IGNORECASE)
        # используем функцию замены подстрок в строке
        # функция lambda оставляет первый символ слова и заменяет оставшиеся на *
        value = re.sub(pattern, lambda match: match.group()[0] + '*' * (len(match.group()) - 1), value)
    return value
