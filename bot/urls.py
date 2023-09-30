from django.urls import path
from . import views

urlpatterns = [
    path('telegram_webhook/', views.telegram_webhook, name='telegram_webhook'),
    path('send_message/', views.send_message, name='send_message'),
    path('get_messages/', views.get_messages, name='get_messages'),
]
