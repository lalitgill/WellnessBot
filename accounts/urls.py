from django.urls import path
from .views import LoginView, LogoutView
from django.contrib.auth.views import LogoutView
from .views import *
from django.conf import settings

def logout_then_login(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect(settings.LOGIN_URL)

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    #path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    #path('logout/', LogoutView.as_view(), name='logout'),
    #path('logout/', LogoutView.as_view(), name='logout'),
    path('logout/', logout_then_login, name='logout'),
    path('register/', register_user, name='register_user'),
]