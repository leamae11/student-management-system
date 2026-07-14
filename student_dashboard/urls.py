"""
URL configuration for student_dashboard project.
"""
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # API Endpoints
    path('api/users/', include('users.urls')),
    path('api/tasks/', include('tasks.urls')),
    path('api/grades/', include('grades.urls')),
    path('api/notes/', include('notes.urls')),
    path('api/ojt/', include('ojt.urls')),
    path('api/requirements/', include('requirements_app.urls')),
]
