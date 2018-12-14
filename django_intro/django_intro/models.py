from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    username = models.CharField(max_length=50)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=200)
    favorites = models.ManyToManyField(
        "Recipe", symmetrical=False, related_name="favorites")

    def __str__(self):
        return self.username


class Recipe(models.Model):
    title = models.CharField(max_length=100)
    instructions = models.TextField(max_length=2000)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    description = models.TextField(max_length=200)
    time_required = models.FloatField()

    def __str__(self):
        return self.title
