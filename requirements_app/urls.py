from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SchoolRequirementViewSet

router = DefaultRouter()
router.register(r'', SchoolRequirementViewSet, basename='requirement')

urlpatterns = [
    path('', include(router.urls)),
]
