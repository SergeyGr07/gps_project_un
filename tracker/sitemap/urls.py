from django.urls import path
from .import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('map/', views.map, name = 'map'),
    path('map/chat/', views.chat, name = 'chat'),
    path('send-message/', views.send_message, name='send_message'),
]
