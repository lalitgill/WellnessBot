from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.file_upload, name='file_upload'),
    path('files/', views.file_list, name='file_list'),
    path('files/<int:file_id>/edit/', views.file_edit, name='file_edit'),

]