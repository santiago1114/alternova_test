from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StreamViewSet

router = DefaultRouter()
router.register('stream', StreamViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
]
