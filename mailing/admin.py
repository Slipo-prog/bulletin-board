from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path
from .models import Mailing
from .tasks import send_newsletter


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ['subject', 'created_at', 'sent_at', 'recipient_count']
    filter_horizontal = ['recipients']
    actions = ['send_mailing']

    def recipient_count(self, obj):
        return obj.recipients.count()

    recipient_count.short_description = 'Количество получателей'

    def send_mailing(self, request, queryset):
        for mailing in queryset:
            send_newsletter.delay(mailing.id)
        self.message_user(request, f'Рассылка запущена для {queryset.count()} кампаний')
        return HttpResponseRedirect(request.get_full_path())

    send_mailing.short_description = 'Отправить выбранные рассылки'