from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<sender_number>\w+)/(?P<receiver_number>\w+)/$', consumers.ChatConsumer.as_asgi()),
]