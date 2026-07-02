from django.core.management.base import BaseCommand
from posts.models import Category


class Command(BaseCommand):
    help = 'Создает категории для объявлений'

    def handle(self, *args, **options):
        categories = [
            'Танки', 'Хилы', 'ДД', 'Торговцы',
            'Гилдмастеры', 'Квестгиверы', 'Кузнецы',
            'Кожевники', 'Зельевары', 'Мастера заклинаний'
        ]

        for cat in categories:
            Category.objects.get_or_create(name=cat)
            self.stdout.write(f'✅ Создана категория: {cat}')

        self.stdout.write(self.style.SUCCESS('✅ Все категории созданы!'))