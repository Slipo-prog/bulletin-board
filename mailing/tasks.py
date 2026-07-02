from celery import shared_task
from django.core.mail import send_mass_mail
from django.conf import settings
from django.utils import timezone
from .models import Mailing


@shared_task
def send_newsletter(mailing_id):
    """Отправляет массовую рассылку"""
    try:
        mailing = Mailing.objects.get(id=mailing_id)
        users = mailing.recipients.all()

        # Если получатели не указаны, отправляем всем активным пользователям
        if not users:
            from accounts.models import User
            users = User.objects.filter(is_active=True, is_email_verified=True)

        # Формируем список сообщений
        messages = []
        for user in users:
            messages.append((
                mailing.subject,
                f"{mailing.body}\n\n---\nЗдравствуйте, {user.email}!",
                settings.DEFAULT_FROM_EMAIL,
                [user.email]
            ))

        # Отправляем массово
        send_mass_mail(messages, fail_silently=False)

        # Обновляем дату отправки
        mailing.sent_at = timezone.now()
        mailing.save()

        return f"Рассылка #{mailing_id} отправлена {len(messages)} пользователям"
    except Mailing.DoesNotExist:
        return f"Рассылка #{mailing_id} не найдена"