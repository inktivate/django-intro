from django.shortcuts import render, HttpResponseRedirect, reverse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required


from django_intro.models import Recipe, Author
from django_intro.forms import AuthorForm, RecipeForm, LoginForm, RecipeEditForm


def get_item(request):
    id = int(request.GET.get('id'))
    return id


def recipe_view(request):
    recipe_id = get_item(request)
    recipe = Recipe.objects.filter(id=recipe_id)
    return render(request, 'recipe_view.html', {'data': recipe, 'user': request.user})


def index_view(request):
    recipes = Recipe.objects.all()
    author = Author.objects.filter(user=request.user).first()
    return render(request, 'index_view.html', {
        'data': recipes,
        'user': request.user,
        'author': author,
    })


def author_view(request):
    author_id = get_item(request)
    author = Author.objects.filter(id=author_id).first()
    recipes = Recipe.objects.filter(author=author_id)
    favorites = author.favorites.all()
    return render(request, 'author_view.html', {
        'author': author,
        'recipes': recipes,
        'favorites': favorites,
    })


@login_required()
def new_author(request):
    form = AuthorForm(None or request.POST)
    if form.is_valid():
        data = form.cleaned_data
        user = User.objects.create_user(
            data['username'], data['email'], data['password'])
        Author.objects.create(
            username=data['username'],
            bio=data['bio'],
            user=user,
        )
        return HttpResponseRedirect(reverse('homepage'))
    return render(request, 'author_form.html', {
        'form': form, 'user': request.user
    })


@login_required()
def new_recipe(request):
    html = 'recipe_form.html'
    form = None
    if request.method == 'POST':
        form = RecipeForm(request.user, request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Recipe.objects.create(
                author=Author.objects.filter(id=data['author']).first(),
                title=data['title'],
                instructions=data['instructions'],
                description=data['description'],
                time_required=data['time_required']
            )
            return HttpResponseRedirect(reverse('homepage'))
    else:
        form = RecipeForm(request.user)
    return render(request, html, {'form': form})


def login_view(request):
    form = LoginForm(None or request.POST)
    if form.is_valid():
        next = request.POST.get('next')
        data = form.cleaned_data
        user = authenticate(
            username=data['username'],
            password=data['password']
        )
        if user is not None:
            login(request, user)
            if next:
                return HttpResponseRedirect(next)
            else:
                return HttpResponseRedirect(reverse('homepage'))
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('homepage'))


def recipe_fav(request):
    recipe_id = get_item(request)
    recipe = Recipe.objects.filter(id=recipe_id).first()
    user = Author.objects.filter(user_id=request.user.id).first()
    user.favorites.add(recipe)
    print(user.favorites.all())
    return HttpResponseRedirect('/recipe/?id=' + str(recipe_id))


def recipe_unfav(request):
    recipe_id = get_item(request)
    recipe = Recipe.objects.filter(id=recipe_id).first()
    user = Author.objects.filter(user_id=request.user.id).first()
    user.favorites.remove(recipe)
    print(user.favorites.all())
    return HttpResponseRedirect('/recipe/?id=' + str(recipe_id))


@login_required()
def recipe_edit(request):
    recipe_id = get_item(request)
    recipe = Recipe.objects.filter(id=recipe_id).first()
    html = 'recipe_edit.html'
    form = None
    if request.method == 'POST':
        form = RecipeEditForm(request.user, request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Recipe.objects.filter(id=recipe_id).update(
                title=data['title'],
                instructions=data['instructions'],
                description=data['description'],
                time_required=data['time_required']
            )
            return HttpResponseRedirect(reverse('homepage'))
    else:
        form = RecipeEditForm(request.user, initial={
            'title': recipe.title,
            'instructions': recipe.instructions,
            'description': recipe.description,
            'time_required': recipe.time_required,
        })
    return render(request, html, {
        'form': form,
        'recipe': recipe,
        'user': request.user
    })
