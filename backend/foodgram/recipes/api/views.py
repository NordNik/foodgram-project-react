from rest_framework import viewsets, filters, permissions
from rest_framework.permissions import IsAuthenticated

from recipes.models import Recipes, Tag
from .paginator import paginate_page
from .serializers import RecipesSerializer, TagsSerializer


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipes.objects.all()
    serializer_class = RecipesSerializer
    #paginator = [paginate_page]
    #permission_classes = [IsAuthenticated]


class TagsViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagsSerializer
    permission_classes = (permissions.AllowAny, )
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name',)
    #lookup_field = 'slug' #with it cannot reach it by id only by slug
