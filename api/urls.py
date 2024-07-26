from django.urls import path, include

app_name = 'api'

urlpatterns = [
    #path('', include('framework.urls')),
    path('users/', include('users.urls')),
    path('reportocr/', include('reportocr.urls')),
    #path('dashboard/', include('dashboard.urls'))
]