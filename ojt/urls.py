from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OJTRequirementViewSet, OJTLogViewSet

router = DefaultRouter()
router.register(r'requirements', OJTRequirementViewSet, basename='ojt-requirement')
router.register(r'logs', OJTLogViewSet, basename='ojt-log')

urlpatterns = [
    path('', include(router.urls)),
]
