# plant_identification/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('identify/', views.identify_plant_view, name='identify_plant'),
]
