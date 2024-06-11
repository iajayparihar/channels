from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/sc/<str:groupName>/', consumers.ChatSyncConsumer.as_asgi()),
    path('ws/ac/<str:groupName>/', consumers.ChatASyncConsumer.as_asgi()),
]
