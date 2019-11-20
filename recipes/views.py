from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import render, redirect
import requests, os
from .models import Recipe
from django.views.decorators.csrf import csrf_protect


def recipes(request):
    app_id = os.environ.get('APP_ID')
    app_key = os.environ.get('APP_KEY')
    results = []
    if request.method == 'POST':
        # check for dietary restrictions
        restrictions = request.POST.getlist('restrictions')
        # format input ingredients
        raw_input = request.POST['ingredients']
        pantry = raw_input.split(',')
        for index in range(len(pantry)):
            pantry[index] = pantry[index].strip()
        response = requests.get('https://api.edamam.com/search',
                                params={'q': f"{' '.join(pantry)}", 'app_id': app_id, 'health': restrictions,
                                        'app_key': app_key, 'to': 100})
        try:
            response.raise_for_status()
        except requests.exceptions.RequestException:
            return render(request, 'recipes/recipes.html', {'error': 'An error occurred searching for your recipes.'})

        # determines how many ingredients required in the recipe we are missing
        pantry.extend(['salt', 'water', 'black pepper'])
        for hit in response.json()['hits']:
            all_ingredients = get_ingredients(hit['recipe']['ingredients'])
            all_ingredients = lower_case(all_ingredients)
            stocked_index = []
            for ingredient in pantry:
                for count, ingredient_line in enumerate(all_ingredients):
                    if ingredient in ingredient_line and count not in stocked_index:
                        stocked_index.append(count)
                        break

            needed_ingredients = remove_stocked_items(all_ingredients, stocked_index)
            # set recipe model attributes
            recipe = Recipe()
            recipe.set_fields(hit, len(needed_ingredients))
            results.append(recipe)

        results = sorted(results, key=lambda x: x.missing_count)

        return render(request, 'recipes/recipes.html', {'results': results})

    else:
        return render(request, 'recipes/recipes.html', {'error': 'Please search for a recipe'})


def lower_case(words):
    return [word.lower() for word in words]


def get_ingredients(raw_data):
    formatted = []
    for index in range(len(raw_data)):
        formatted.append(raw_data[index]['text'])
    return formatted


def remove_stocked_items(total, have):
    for index in sorted(have, reverse=True):
        del total[index]
    return total


@csrf_protect
def add(request):
    if request.method == 'POST':
        '''title = request.POST['title']
        image = request.POST['image']
        source = request.POST['source']
        '''
        title = request.POST['title']
        image = request.POST['image']
        source = request.POST['source']
        user = request.user
        try:
            recipe = Recipe.objects.get(image=image, title=title, source=source)
        except ObjectDoesNotExist:
            recipe = Recipe.objects.create(image=image, title=title, source=source)
        finally:
            recipe.users.add(user)  # won't do anything if current user is already in the query set
            recipe.save()
        same_url = request.POST.get('next', '/')
        return redirect('/accounts/myrecipes/')
    else:
        return JsonResponse({'success': False})