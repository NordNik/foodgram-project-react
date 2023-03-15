from django.db.models import Sum
from django.http.response import HttpResponse
from rest_framework import viewsets, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import action
from rest_framework import status
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response

from users.models import User
from recipes.models import Recipes, Tag, Ingredient
from .permissions import RecipePermission
from .serializers import (
    IngredientsSerializer, RecipesSerializer, TagsSerializer,
    UsersSerializer, MyTokenObtainPairSerializer, RegisterSerializer,
    RecipesGetSerializer, IngredientRecipes, ShoppingFavoriteSerializer,
    UserAuthSerializer, SetPasswordSerializer)


def add_or_delete(request, pk, param, serializer):
    """create actions for favorite and shopping cart endpoints"""
    _objects = param
    if_obj = _objects.filter(pk=pk).exists()
    if request.method == 'DELETE' and if_obj:
        _objects.clear()
        return Response(status=status.HTTP_204_NO_CONTENT)
    if request.method == 'POST' and not if_obj:
        _objects.add(pk)
        _serializer = serializer(
            _objects.get(pk=pk),
            context={'request': request}
        )
        return Response(_serializer.data, status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)


class RecipesViewSet(viewsets.ModelViewSet):
    """Allows to operate with recipes"""
    queryset = Recipes.objects.all()
    serializer_class = RecipesSerializer
    permission_classes = [RecipePermission]
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter,)
    filterset_fields = ('tags',)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH',):
            return RecipesSerializer
        return RecipesGetSerializer

    @action(methods=['POST', 'DELETE'], detail=True)
    def favorite(self, request, pk):
        """Add or delete recipe to/from list of favorites"""
        return add_or_delete(
            request,
            pk,
            request.user.is_favorited,
            ShoppingFavoriteSerializer)

    @action(methods=['POST', 'DELETE'], detail=True)
    def shopping_cart(self, request, pk):
        """Add or delete recipe to/from shopping cart"""
        return add_or_delete(
            request,
            pk,
            request.user.shopping_cart,
            ShoppingFavoriteSerializer)

    @action(methods=['GET'], detail=False)
    def download_shopping_cart(self, request):
        """Return a file with the list of ingredients from favorite recipes"""
        # extract data from favorite recipes
        shop_recipes = request.user.shopping_cart.all()
        ingredients = IngredientRecipes.objects.filter(
            recipe__in=shop_recipes
        ).values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).annotate(sum_amount=Sum('amount'))

        # create file text in format "ingredient (unit) - amount"
        ingredients_list_text = 'Below is your shopping list for today:\n'
        for _ingredient in ingredients:
            name = _ingredient.get('ingredient__name')
            m_unit = _ingredient.get('ingredient__measurement_unit')
            amount = _ingredient.get('sum_amount')
            ingredients_list_text += f'{name} ({m_unit}) - {amount}\n'
        ingredients_list_text += 'Enjoy your meal!'

        # return the file
        filename = f'Shopping_list_{request.user.username}.txt'
        response = HttpResponse(
            ingredients_list_text, content_type='text/plain')
        response['Content-Disposition'] = (
            f'attachment; filename="{filename}"'
        )
        return response


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    """Allows to operate with ingredients"""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientsSerializer
    permission_classes = (permissions.AllowAny, )
    filter_backends = (DjangoFilterBackend,)
    search_fields = ('name',)


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    """Allows to operate with tags"""
    queryset = Tag.objects.all()
    serializer_class = TagsSerializer
    permission_classes = (permissions.AllowAny, )


class UsersViewSet(viewsets.ModelViewSet):
    """Allows to operate with users"""
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH',):
            return RegisterSerializer
        return UsersSerializer

    @action(
        methods=['POST'],
        detail=False,
        permission_classes=[permissions.IsAuthenticated])
    def set_password(self, request):
        """Allows to change password if current password is right"""
        print(request.user.password)
        print(request.data)
        user = request.user
        serializer = SetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            current_password = serializer.data.get('current_password')
            if not user.check_password(current_password):
                content = {'current_password': 'Wrong current password'}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(serializer.data.get('new_password'))
            user.save()
            content = {'Password has been changed succesfully'}
            return Response(content, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST', 'DELETE'], detail=True)
    def subscribe(self, request, pk):
        """Add or delete subscription"""
        _follower = self.get_object()
        if request.user == _follower:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return add_or_delete(
            request,
            pk,
            request.user.followers,
            UserAuthSerializer)

    @action(methods=['GET'], detail=False)
    def subscriptions(self, request):
        """Allows to get list of subscribes"""
        user = request.user
        followers = user.followers.all()
        pages = self.paginate_queryset(followers)
        serializer = UsersSerializer(
            pages, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)


class MyObtainTokenPairView(TokenObtainPairView):
    """Provides tokens"""
    permission_classes = (permissions.AllowAny,)
    serializer_class = MyTokenObtainPairSerializer
