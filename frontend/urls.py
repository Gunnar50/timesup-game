from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('csrf/', views.csrf, name='csrf'),
    path('room/<int>:id/', views.index),
    path('join-room/', views.index),
    path('create-room/', views.index),
]