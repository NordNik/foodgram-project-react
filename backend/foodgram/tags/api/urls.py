from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import TagsViewSet

tags_router = DefaultRouter()
tags_router.register('', TagsViewSet, basename='tags')

urlpatterns = [
    path('', include(tags_router.urls)),
]