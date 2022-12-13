from django.urls import include, path

from . import views


urlpatterns = [
    path('', views.index),
    path('recipes/', views.recipes_list),
    path('recipes/<slug:pk>/', views.recipes_detail),
]
