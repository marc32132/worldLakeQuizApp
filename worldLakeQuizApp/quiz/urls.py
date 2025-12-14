from django.urls import path
from . import views

app_name = 'quiz'

urlpatterns = [
    path('', views.quiz_lakes, name="quiz_lakes"),
    path('results/', views.quiz_results, name="quiz_results"),
]
