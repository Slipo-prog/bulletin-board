from django.db import models
from django.conf import settings
from posts.models import Post


class Response(models.Model):
    """
    Модель отклика на объявление
    """
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='responses',
        verbose_name='Объявление'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Автор отклика'
    )
    text = models.TextField(verbose_name='Текст отклика')
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    is_accepted = models.BooleanField(
        default=False,
        verbose_name='Принят'
    )

    class Meta:
        verbose_name = 'Отклик'
        verbose_name_plural = 'Отклики'
        ordering = ['-created_at']

    def __str__(self):
        return f'Отклик на "{self.post.title}" от {self.author.email}'