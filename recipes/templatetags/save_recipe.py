from django import template
from recipes.models import Recipe

register = template.Library()


@register.simple_tag
def save_recipe(result, user):
    result.save_model(user)
