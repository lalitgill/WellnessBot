"""
URL configuration for wellnessbot project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include, path
from rest_framework_simplejwt import views as jwt_views
from django.conf.urls.static import static
from django.conf import settings
from dashboard.views import DashboardView, AddItemView, DeleteItemView

admin.site.site_header = "Your Dashboard"
admin.site.site_title = "Your Dashboard Portal"
admin.site.index_title = "Welcome to Your Dashboard Portal"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', DashboardView.as_view(), name='dashboard'),
    path('add/', AddItemView.as_view(), name='add_item'),
    path('delete/<int:pk>/', DeleteItemView.as_view(), name='delete_item'),

    path('accounts/', include('accounts.urls')),
    path('uploadreports/', include('uploadreports.urls')),
    path('chatbot/', include('chatbot.urls')),

    path('v1/api/token/login/',jwt_views.TokenObtainPairView.as_view(), name ='token_obtain_pair'),
    path('v1/api/token/login/refresh/',jwt_views.TokenRefreshView.as_view(),name ='token_refresh'),
    path('v1/api/', include('api.urls', namespace='Api')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)