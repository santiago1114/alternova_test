from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StreamViewSet, TypeViewSet, GenreViewSet, UserRegistrationView

router = DefaultRouter()
router.register('genre', GenreViewSet)
router.register('type', TypeViewSet)
router.register('stream', StreamViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
]
