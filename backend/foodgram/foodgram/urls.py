from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'api/auth/', include('djoser.urls.authtoken')),
    #path(r'auth/', include('djoser.urls.jwt')),
    #path('api/auth/', include('django.contrib.auth.urls')),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/users/', include('users.api.urls')),
    path('api/recipes/', include('recipes.api.urls')),
    path('api/tags/', include('tags.api.urls')),
]
