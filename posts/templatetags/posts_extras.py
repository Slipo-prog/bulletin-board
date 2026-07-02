from django import template
from posts.models import Post

register = template.Library()

@register.filter
def get_post_title(post_id):
    """Возвращает заголовок объявления по его ID"""
    try:
        post = Post.objects.get(id=post_id)
        return post.title
    except Post.DoesNotExist:
        return "Объявление не найдено"