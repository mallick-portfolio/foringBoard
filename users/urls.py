
from django.urls import path, include
from .views import RegisterView, LoginView, UserViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
   path('users/register/', RegisterView.as_view(), name='register'),
   path('users/login/', LoginView.as_view(), name='login'),
   path('', include(router.urls)),
]
