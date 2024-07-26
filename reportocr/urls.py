from django.urls import path
from reportocr import views
import platform

urlpatterns = [
    path('upload-image', views.UploadImages.as_view()),
]