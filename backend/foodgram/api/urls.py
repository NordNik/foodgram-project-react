from django.urls import include, path
from rest_framework.routers import DefaultRouter

#from .v1.urls import auth_url_pattern_list
from .v1.views import RecipesViewSet

v1_router = DefaultRouter()
v1_router.register('recipes', RecipesViewSet, basename='recipes')
#v1_router.register(
#    r'recipes/(?P<title_id>\d+)/comments',
#    ReviewViewSet,
#    basename='reviews'
#)
#v1_router.register(
#    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
#    CommentViewSet,
#    basename='comments'
#)

urlpatterns = [
    #path('v1/auth/', include(auth_url_pattern_list)),
    path('v1/', include(v1_router.urls))
]
