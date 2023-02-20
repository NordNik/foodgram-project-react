from rest_framework import viewsets, filters, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import User
from .permissions import IsAutheticatedOrRegistration
from recipes.models import Recipes, Tag, Ingredient
from .paginator import UsersPagination, paginate_page
from .serializers import (
    IngredientsSerializer, RecipesSerializer, TagsSerializer,
    UsersSerializer, MyTokenObtainPairSerializer, RegisterSerializer,
    RecipesGetSerializer)


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipes.objects.all()
    serializer_class = RecipesSerializer
    # paginator = [paginate_page]
    # permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH',):
            return RecipesSerializer
        return RecipesGetSerializer


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientsSerializer
    permission_classes = (permissions.AllowAny, )
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name',)


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagsSerializer
    permission_classes = (permissions.AllowAny, )
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name',)
    # lookup_field = 'slug' #with it cannot reach it by id only by slug


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = UsersPagination

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH',):
            return RegisterSerializer
        return UsersSerializer


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = MyTokenObtainPairSerializer
