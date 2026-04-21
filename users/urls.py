"""
URL routing for the users app.

Routes:
- 'signup/' (signup_view): user registration page
- 'login/' (LoginView): authentication interface using standard Django auth
- 'logout/' (LogoutView): logs out the user and redirects
"""
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users'

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
