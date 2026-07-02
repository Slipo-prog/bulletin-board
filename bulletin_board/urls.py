from django.contrib import admin
from django.urls import path, include  # ВАЖНО: include должен быть импортирован
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),  # Для регистрации
    path('posts/', include('posts.urls')),       # Для объявлений
    path('responses/', include('responses.urls')), # Для откликов
    path('', include('posts.urls')),             # Главная страница
]

# Для отображения загруженных файлов (картинок) в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)