from django.urls import path
from chat import consumers
websocket_urlpatterns = [
    path(r'ws/chat/<int:id>/', consumers.ChatConsumer.as_asgi()),
]