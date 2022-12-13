from django.http import HttpResponse
from django.shortcuts import render

from .models import Recipes
from .paginator import paginate_page


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


def recipes_list(request):
    return HttpResponse('Recipes list')


def recipes_detail(request, pk):
    return HttpResponse('Certain recipe')