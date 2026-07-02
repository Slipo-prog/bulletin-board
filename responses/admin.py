from django.contrib import admin
from .models import Response


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ['id', 'post', 'author', 'text_preview', 'created_at', 'is_accepted']
    list_filter = ['is_accepted', 'created_at', 'post__category']
    search_fields = ['post__title', 'author__email', 'text']
    list_editable = ['is_accepted']
    readonly_fields = ['created_at']

    def text_preview(self, obj):
        """Показывает первые 50 символов текста"""
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text

    text_preview.short_description = 'Текст (предпросмотр)'

    fieldsets = (
        ('Основная информация', {
            'fields': ('post', 'author', 'text')
        }),
        ('Статус', {
            'fields': ('is_accepted',)
        }),
        ('Дата', {
            'fields': ('created_at',)
        }),
    )