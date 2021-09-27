from django.contrib import admin
from django.urls import path
from app.views import health_check


urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', health_check)
]
