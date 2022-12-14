from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Recipes
from .paginator import paginate_page
from .serializers import RecipesSerializer


def index(request):
    """Shows latest posts on main page"""
    #recipes_list = Recipes.objects.select_related('pub_date', 'group')
    #page_obj = paginate_page(request, recipes_list)
    #return render(
    #    request,
    #    'posts/index.html',
    #    context={'page_obj': page_obj, }
    #)
    return HttpResponse('Recipes list')


@api_view(['GET', 'POST'])
def recipes_list(request):
    if request.method == 'POST':
        serializer = RecipesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    recipes = Recipes.objects.all()
    serializer = RecipesSerializer(recipes, many=True)
    return Response(serializer.data) 
    #return HttpResponse('Recipes list')


def recipes_detail(request, pk):
    return HttpResponse('Certain recipe')