from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from recipes.models import Recipes
from .paginator import paginate_page
from .serializers import RecipesSerializer


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipes.objects.all()
    serializer_class = RecipesSerializer
    #paginator = [paginate_page]
    permission_classes = [IsAuthenticated]