from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    RecipesViewSet, IngredientsViewSet, TagsViewSet,
    MyObtainTokenPairView, UsersViewSet)


recipes_router = DefaultRouter()
recipes_router.register('recipes', RecipesViewSet, basename='users')
recipes_router.register(
    'ingredients',
    IngredientsViewSet,
    basename='ingredients')
recipes_router.register('tags', TagsViewSet, basename='tags')

urlpatterns = [
    path('', include(recipes_router.urls))
]


users_router = DefaultRouter()
users_router.register('', UsersViewSet, basename='users')
users_router.register('register', UsersViewSet, basename='register')

urlpatterns = [
    path('', include(users_router.urls)),
    path('login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
