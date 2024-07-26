from django.urls import path
from users import views
import uuid
#from users.views import CustomTokenObtainPairView

app_name = 'users'

urlpatterns = [
    path('token/login', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('create', views.CreateUser.as_view()),
    path('edit', views.EditUser.as_view()),
    path('delete', views.DeleteUser.as_view()),
    path('list', views.ClientUsersList.as_view()),
    path('details', views.UsersDetails.as_view()),
    #path('change/password/', views.ChangeUserPassword.as_view()),
    path('reset_password', views.ResetPassword.as_view()),
    ##https://studygyaan.com/django/django-rest-framework-tutorial-change-password-and-reset-password
]