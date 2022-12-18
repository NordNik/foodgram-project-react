from django.http import HttpResponse
from rest_framework import viewsets


from recipes.models import Recipes
from .paginator import paginate_page
from .serializers import RecipesSerializer


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipes.objects.all()
    serializer_class = RecipesSerializer 

def index(request):
    """Shows latest posts on main page"""
    return HttpResponse('Recipes list')
