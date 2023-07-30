from django.urls import path

from .consumers import GameConsumer  # The consumers module will be defined later

ws_urlpatterns = [
    # path(r'ws/game/(?P<room_code>\w+)/$', GameConsumer.as_asgi()),  # 'ws/game/ROOM_CODE/'
    path('ws/game/room/<room_code>/', GameConsumer.as_asgi(), name="room"),  # 'ws/game/ROOM_CODE/'
    # path('ws/game/', GameConsumer.as_asgi()),  # 'ws/game/ROOM_CODE/'
]



