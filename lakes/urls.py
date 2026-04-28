"""
URL routing for the lakes app.

Routes:
- '' (lake_info): displays all lakes in the database
"""
from django.urls import path
from . import views

app_name = 'lakes'

urlpatterns = [
    path('', views.lake_info, name="list"),
]
