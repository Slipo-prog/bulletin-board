from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.contrib import messages
from .models import Response
from .forms import ResponseForm
from .tasks import send_response_notification, send_accept_notification  # ИМПОРТ ЗАДАЧ
from posts.models import Post


class MyResponsesView(LoginRequiredMixin, ListView):
    """
    Приватная страница с откликами на объявления пользователя
    """
    model = Response
    template_name = 'responses/my_responses.html'
    context_object_name = 'responses'

    def get_queryset(self):
        """
        Фильтруем отклики:
        - Только на объявления текущего пользователя
        - Можно фильтровать по конкретному объявлению (post_id)
        """
        qs = Response.objects.filter(post__author=self.request.user).order_by('-created_at')
        post_id = self.request.GET.get('post_id')
        if post_id:
            qs = qs.filter(post_id=post_id)
        return qs

    def get_context_data(self, **kwargs):
        """
        Добавляем список объявлений пользователя для фильтра
        """
        context = super().get_context_data(**kwargs)
        context['user_posts'] = Post.objects.filter(author=self.request.user)
        return context


class ResponseCreateView(LoginRequiredMixin, CreateView):
    """
    Создание отклика на объявление
    """
    model = Response
    form_class = ResponseForm
    template_name = 'responses/response_form.html'

    def form_valid(self, form):
        """
        При сохранении отклика:
        1. Привязываем отклик к объявлению
        2. Указываем автора отклика
        3. Отправляем уведомление автору объявления
        """
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        form.instance.post = post
        form.instance.author = self.request.user
        response = form.save()

        # Отправка уведомления автору объявления (асинхронно через Celery)
        send_response_notification.delay(response.id)

        # Добавляем сообщение об успехе
        messages.success(self.request, f'Ваш отклик на "{post.title}" успешно отправлен!')

        return super().form_valid(form)

    def get_success_url(self):
        """
        После успешного создания перенаправляем на страницу объявления
        """
        return reverse_lazy('posts:post_detail', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        """
        Добавляем объявление в контекст для шаблона
        """
        context = super().get_context_data(**kwargs)
        context['post'] = get_object_or_404(Post, pk=self.kwargs['pk'])
        return context


class ResponseAcceptView(LoginRequiredMixin, UpdateView):
    """
    Принятие отклика
    """
    model = Response
    fields = []  # Никаких полей для редактирования
    template_name = 'responses/response_confirm.html'
    success_url = reverse_lazy('responses:my_responses')

    def get_object(self, queryset=None):
        """
        Проверяем, что пользователь - автор объявления
        """
        obj = super().get_object(queryset)
        if obj.post.author != self.request.user:
            raise Http404("Вы не можете принять этот отклик")
        return obj

    def form_valid(self, form):
        """
        При принятии отклика:
        1. Меняем статус is_accepted на True
        2. Отправляем уведомление автору отклика
        """
        form.instance.is_accepted = True
        response = form.save()

        # Отправка уведомления автору отклика (асинхронно через Celery)
        send_accept_notification.delay(response.id)

        # Добавляем сообщение об успехе
        messages.success(self.request, f'Отклик от {response.author.email} успешно принят!')

        return super().form_valid(form)


class ResponseDeleteView(LoginRequiredMixin, DeleteView):
    """
    Удаление отклика
    """
    model = Response
    template_name = 'responses/response_confirm_delete.html'
    success_url = reverse_lazy('responses:my_responses')

    def get_object(self, queryset=None):
        """
        Проверяем, что пользователь - автор объявления
        """
        obj = super().get_object(queryset)
        if obj.post.author != self.request.user:
            raise Http404("Вы не можете удалить этот отклик")
        return obj

    def delete(self, request, *args, **kwargs):
        """
        Добавляем сообщение при удалении
        """
        response = self.get_object()
        messages.success(self.request, f'Отклик от {response.author.email} успешно удален!')
        return super().delete(request, *args, **kwargs)