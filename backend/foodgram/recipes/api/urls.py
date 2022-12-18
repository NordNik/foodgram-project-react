from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import RecipesViewSet

users_router = DefaultRouter()
users_router.register('', RecipesViewSet, basename='users')

urlpatterns = [
    path('', include(users_router.urls))
]