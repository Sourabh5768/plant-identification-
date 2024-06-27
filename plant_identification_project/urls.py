# plant_identification_project/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('plant_identification.urls')),  # Redirect root URL to plant_identification app
]
