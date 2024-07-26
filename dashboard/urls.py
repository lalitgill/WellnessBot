from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('chat/', views.chat, name='chat'),
    path('login/', views.login_view, name='login'),
]