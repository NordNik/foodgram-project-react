from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    RecipesViewSet, IngredientsViewSet, TagsViewSet, UsersViewSet)

foodgram_router = DefaultRouter()
foodgram_router.register('recipes', RecipesViewSet, basename='users')
foodgram_router.register(
    'ingredients', IngredientsViewSet, basename='ingredients')
foodgram_router.register('tags', TagsViewSet, basename='tags')

users_router = DefaultRouter()
users_router.register('users', UsersViewSet, basename='users')
users_router.register('', UsersViewSet, basename='users')
users_router.register('register', UsersViewSet, basename='register')

urlpatterns = [
    path('', include(foodgram_router.urls)),
    path('', include(users_router.urls)),
    path(r'auth/', include('djoser.urls.authtoken')),
]
