from django import forms
from django_intro.models import Author


class AuthorForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    email = forms.CharField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput())
    bio = forms.CharField(widget=forms.Textarea, label='Bio')


class RecipeForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super(RecipeForm, self).__init__(*args, **kwargs)
        author = Author.objects.filter(user=user).first()
        self.fields['author'].choices = [(author.id, author.username)]

    title = forms.CharField(label='Title', max_length=100)
    instructions = forms.CharField(
        widget=forms.Textarea, label='Instructions', max_length=2000)
    author = forms.ChoiceField()
    description = forms.CharField(
        widget=forms.Textarea, label='Description', max_length=200)
    time_required = forms.FloatField()


class RecipeEditForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super(RecipeEditForm, self).__init__(*args, **kwargs)

    title = forms.CharField(label='Title', max_length=100)
    instructions = forms.CharField(
        widget=forms.Textarea, label='Instructions', max_length=2000)
    description = forms.CharField(
        widget=forms.Textarea, label='Description', max_length=200)
    time_required = forms.FloatField()


class LoginForm(forms.Form):
    username = forms.CharField(label='username')
    password = forms.CharField(label='password', widget=forms.PasswordInput())
