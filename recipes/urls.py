from django.urls import path
from recipes import views
from .models import Recipe

urlpatterns = [
    path('add/', views.add, name='add'),
    path('', views.recipes, name='recipes'),
    #path('delete/', views.delete, name='delete'),

    ]