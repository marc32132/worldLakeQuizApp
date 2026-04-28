"""
URL routing for the World Lake Quiz project.

Routes:
- 'admin/': Django admin panel
- '': quiz app main interface
- 'quiz/': quiz app routes
- 'lakes/': lakes app routes
- 'users/': users app routes
"""
from django.contrib import admin
from django.urls import path, include, re_path
from . import views
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage, name='home'),
    path('lake_info/', include('lakes.urls')),
    path('quiz_lakes/', include('quiz.urls')),
    path('users/', include('users.urls')),

    # Serve media and static files in development
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root':settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root':settings.STATIC_ROOT})
]
