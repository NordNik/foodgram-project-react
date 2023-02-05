from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    MyObtainTokenPairView, UsersViewSet)

users_router = DefaultRouter()
users_router.register('', UsersViewSet, basename='users')
users_router.register('register', UsersViewSet, basename='register')

urlpatterns = [
    path('', include(users_router.urls)),
    path('login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]