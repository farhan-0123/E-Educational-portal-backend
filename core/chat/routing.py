from django.urls import re_path

from . import consumers

websockets_urlpatterns = [
    re_path(r'^room/(?P<room_id>\w+)/(?P<username>[\w*d*.*]+)/$', consumers.ChatConsumer.as_asgi())
]