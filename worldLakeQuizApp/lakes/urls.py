from django.urls import path
from . import views

app_name = 'lakes'

urlpatterns = [
    path('', views.lake_info, name="list"),
]
