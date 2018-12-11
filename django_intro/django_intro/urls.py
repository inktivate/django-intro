"""django_intro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import re_path
from django_intro.views import (recipe_view, index_view, author_view,
                                new_author, new_recipe, login_view,
                                logout_view)
from django_intro.models import Author, Recipe

admin.site.register(Author)
admin.site.register(Recipe)

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^recipe/$', recipe_view),
    re_path(r'^author/$', author_view),
    path('', index_view, name='homepage'),
    path('newauthor/', new_author, name='newauthor'),
    path('newrecipe/', new_recipe, name='newrecipe'),
    path('login/', login_view),
    path('logout/', logout_view)
]
