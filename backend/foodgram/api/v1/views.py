from django.db.models import Sum
from django.http.response import HttpResponse
from rest_framework import viewsets, filters, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response


from users.models import User
# from .permissions import IsAutheticatedOrRegistration
from recipes.models import Recipes, Tag, Ingredient
from .paginator import UsersPagination  # paginate_page
from .serializers import (
    IngredientsSerializer, RecipesSerializer, TagsSerializer,
    UsersSerializer, MyTokenObtainPairSerializer, RegisterSerializer,
    RecipesGetSerializer, IngredientRecipes, ShoppingCartSerializer)


class RecipesViewSet(viewsets.ModelViewSet):
    """Allows to operate with recipes"""
    queryset = Recipes.objects.all()
    serializer_class = RecipesSerializer
    # paginator = [paginate_page]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH',):
            return RecipesSerializer
        return RecipesGetSerializer

    @action(methods=['POST', 'DELETE'], detail=True)
    def shopping_cart(self, request, pk):
        """Add or delete recipe to/from shopping cart"""
        shopping_list = request.user.shopping_cart
        if_obj = shopping_list.filter(pk=pk).exists()
        if request.method == 'DELETE' and if_obj:
            shopping_list.clear()
            return Response(status=status.HTTP_204_NO_CONTENT)
        if request.method == 'POST' and not if_obj:
            shopping_list.add(pk)
            serializer = ShoppingCartSerializer(
                shopping_list.get(pk=pk),
                context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['GET'], detail=False)
    def download_shopping_cart(self, request):
        """Return a file with the list of ingredients from favorite recipes"""
        # extract data from favorite recipes
        fav_recipes = request.user.shopping_cart.all()
        ingredients = IngredientRecipes.objects.filter(
            recipe__in=fav_recipes
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
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name',)


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    """Allows to operate with tags"""
    queryset = Tag.objects.all()
    serializer_class = TagsSerializer
    permission_classes = (permissions.AllowAny, )
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name',)


class UsersViewSet(viewsets.ModelViewSet):
    """Allows to operate with users"""
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = UsersPagination

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH',):
            return RegisterSerializer
        return UsersSerializer


class MyObtainTokenPairView(TokenObtainPairView):
    """Provides tokens"""
    permission_classes = (permissions.AllowAny,)
    serializer_class = MyTokenObtainPairSerializer
