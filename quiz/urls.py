"""
URL routing for the quiz app.

Routes:
- '' (quiz_lakes): main quiz interface (GET/POST)
- 'results/' (quiz_results): displays quiz results
"""
from django.urls import path
from . import views

app_name = 'quiz'

urlpatterns = [
    path('', views.quiz_lakes, name="quiz_lakes"),
    path('results/', views.quiz_results, name="quiz_results"),
    path('my-results/', views.saved_results, name="saved_results"),
    path("my-results/<int:result_id>/", views.result_detail, name="result_detail"),
]
