from django.urls import path
from .views import MessengerWebhookView, send_message_api

urlpatterns = [
    path('webhook/', MessengerWebhookView.as_view(), name='messenger_webhook'),
    path('send_message/', send_message_api, name='send_message_api'),
]