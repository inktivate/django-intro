from django.shortcuts import render, HttpResponseRedirect, reverse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required


from django_intro.models import Recipe, Author
from django_intro.forms import AuthorForm, RecipeForm, LoginForm


def get_item(request):
    id = int(request.GET.get('id'))
    return id


def recipe_view(request):
    recipe_id = get_item(request)
    recipe = Recipe.objects.filter(id=recipe_id)
    return render(request, 'recipe_view.html', {'data': recipe})


def index_view(request):
    recipes = Recipe.objects.all()
    return render(
        request,
        'index_view.html',
        {'data': recipes, 'user': request.user}
        )


def author_view(request):
    author_id = get_item(request)
    author = Author.objects.filter(id=author_id)
    recipes = Recipe.objects.filter(author=author_id)
    return render(request, 'author_view.html',
                  {'data': author, 'recipes': recipes}
                  )


@login_required()
def new_author(request):
    form = AuthorForm(None or request.POST)
    if form.is_valid():
        data = form.cleaned_data
        Author.objects.create(
            username=data['username'],
            bio=data['bio']
        )
        user = User.objects.create_user(
            data['username'],
            data['email'],
            data['password'],
            )
        return HttpResponseRedirect(reverse('homepage'))
    return render(request, 'author_form.html', {'form': form, 'user': request.user})


@login_required()
def new_recipe(request):
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
        return render(request, 'thanks.html')
    else:
        form = RecipeForm(request.user)
    return render(request, 'recipe_form.html', {'form': form})


def login_view(request):
    form = LoginForm(None or request.POST)
    if form.is_valid():
        data = form.cleaned_data
        user = authenticate(
            username=data['username'],
            password=data['password']
            )
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(request.GET.get('next'))
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('homepage'))
