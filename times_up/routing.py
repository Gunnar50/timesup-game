from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path

from your_game_app import consumers  # The consumers module will be defined later

websocket_urlpatterns = [
    re_path(r'ws/game/(?P<room_code>\w+)/$', consumers.GameConsumer.as_asgi()),  # 'ws/game/ROOM_CODE/'
]

application = ProtocolTypeRouter({
    'websocket': URLRouter(
        websocket_urlpatterns
    ),
})
