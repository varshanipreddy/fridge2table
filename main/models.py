from django.db import models

class Ingredient(models.Model):
    name = models.CharField(max_length=100)

class Recipe(models.Model):
    recipeid = models.IntegerField()
    recipename = models.CharField(max_length=200)