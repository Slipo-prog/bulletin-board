from django.urls import path
from . import views

app_name = 'responses'

urlpatterns = [
    # Страница со всеми откликами пользователя
    path('my-responses/', views.MyResponsesView.as_view(), name='my_responses'),

    # Создание отклика на объявление (pk - ID объявления)
    path('create/<int:pk>/', views.ResponseCreateView.as_view(), name='response_create'),

    # Принятие отклика (pk - ID отклика)
    path('accept/<int:pk>/', views.ResponseAcceptView.as_view(), name='response_accept'),

    # Удаление отклика (pk - ID отклика)
    path('delete/<int:pk>/', views.ResponseDeleteView.as_view(), name='response_delete'),
]