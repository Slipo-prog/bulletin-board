from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.sites.models import Site


@shared_task
def send_response_notification(response_id):
    """
    Отправляет уведомление автору объявления о новом отклике
    """
    from .models import Response

    try:
        response = Response.objects.select_related('post__author', 'author').get(id=response_id)

        # Получаем текущий сайт для формирования ссылок
        current_site = Site.objects.get_current()
        site_url = f'http://{current_site.domain}'

        subject = f'Новый отклик на ваше объявление "{response.post.title}"'

        message = f'''
        Здравствуйте!

        Пользователь {response.author.email} оставил отклик на ваше объявление "{response.post.title}".

        Текст отклика:
        {response.text}

        Дата: {response.created_at.strftime("%d.%m.%Y %H:%M")}

        Перейти к объявлению: {site_url}/posts/{response.post.id}/
        Посмотреть все отклики: {site_url}/responses/my-responses/

        С уважением,
        Администрация сайта
        '''

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[response.post.author.email],
            fail_silently=False,
        )

        return f"Уведомление отправлено автору {response.post.author.email} (объявление: {response.post.title})"

    except Response.DoesNotExist:
        return f"Ошибка: Отклик с ID {response_id} не найден"
    except Exception as e:
        return f"Ошибка при отправке уведомления: {str(e)}"


@shared_task
def send_accept_notification(response_id):
    """
    Отправляет уведомление автору отклика о том, что его отклик принят
    """
    from .models import Response

    try:
        response = Response.objects.select_related('post__author', 'author').get(id=response_id)

        # Получаем текущий сайт для формирования ссылок
        current_site = Site.objects.get_current()
        site_url = f'http://{current_site.domain}'

        subject = f'Ваш отклик на "{response.post.title}" принят! 🎉'

        message = f'''
        Здравствуйте!

        Поздравляем! Автор объявления "{response.post.title}" принял ваш отклик!

        Ваш отклик:
        {response.text}

        Дата отправки: {response.created_at.strftime("%d.%m.%Y %H:%M")}

        Перейти к объявлению: {site_url}/posts/{response.post.id}/

        С уважением,
        Администрация сайта
        '''

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[response.author.email],
            fail_silently=False,
        )

        return f"Уведомление отправлено автору отклика {response.author.email} (объявление: {response.post.title})"

    except Response.DoesNotExist:
        return f"Ошибка: Отклик с ID {response_id} не найден"
    except Exception as e:
        return f"Ошибка при отправке уведомления: {str(e)}"