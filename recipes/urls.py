from django.urls import path
from recipes import views
from .models import Recipe

urlpatterns = [
    path('', views.recipes, name='recipes'),
    path('add/', views.add, name='add'),
    #path('delete/', views.delete, name='delete'),

    ]