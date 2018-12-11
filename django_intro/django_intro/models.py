from django.db import models


class Author(models.Model):
    username = models.CharField(max_length=50)
    bio = models.TextField(max_length=200)

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
