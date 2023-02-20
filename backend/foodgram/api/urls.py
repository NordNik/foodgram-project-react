from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .v1.views import (
    RecipesViewSet, IngredientsViewSet, TagsViewSet,
    UsersViewSet, MyObtainTokenPairView, RegisterSerializer)

v1_router = DefaultRouter()
v1_router.register('recipes', RecipesViewSet, basename='users')
v1_router.register('ingredients', IngredientsViewSet, basename='ingredients')
v1_router.register('tags', TagsViewSet, basename='tags')
v1_router.register('users', UsersViewSet, basename='users')


urlpatterns = [
    # path('v1/auth/', include(auth_url_pattern_list)),
    path('', include(v1_router.urls))
]
