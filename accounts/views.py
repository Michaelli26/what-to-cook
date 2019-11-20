from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import logout as django_logout
from django.contrib.auth import login as django_login
from django.contrib.auth.decorators import login_required
from recipes.models import Recipe


def signup(request):
    if request.method == 'POST':
        if request.POST['password'] == request.POST['verifypass']:
            try:
                User.objects.get(username=request.POST['username'])
                return render(request, 'accounts/signup.html', {'error': 'User already taken'})
            except User.DoesNotExist:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password'],
                                                last_name=request.POST['lastname'].capitalize(),
                                                first_name=request.POST['firstname'].capitalize())
                auth.login(request, user=user)
                return redirect('home')
        else:
            return render(request, 'accounts/signup.html', {'error': 'Passwords do not match'})
    else:
        return render(request, 'accounts/signup.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            django_login(request, user)
            return render(request, 'home.html')
        else:
            return render(request, 'accounts/login.html', {'error': 'Invalid login.'})
    else:
        return render(request, 'accounts/login.html')


@login_required
def logout(request):
    if request.method == 'POST':
        django_logout(request)
        return redirect('home')


@login_required
def my_recipes(request):
    current_user = request.user
    saved_recipes = Recipe.objects.filter(users=current_user)
    return render(request, 'accounts/myrecipes.html', {'results': saved_recipes})


def delete(request):
    if request.method == 'POST':
        user = request.user
        recipe_pk = request.POST['pk']
        recipe = Recipe.objects.get(pk=recipe_pk)
        recipe.users.remove(user)
        if not recipe.users.exists():
            recipe.delete()
        same_url = request.POST.get('next', '/')
    return redirect(same_url)