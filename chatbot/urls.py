from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_page, name='chat_page'),
    path('chat/', views.chat_view, name='chat'),
    path('chat-partial/', views.chat_partial, name='chat_partial'),
]