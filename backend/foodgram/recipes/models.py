from datetime import timedelta
from django.db import models
from django.contrib.auth import get_user_model

from tags.models import Tag
from users.models import User
        

class Recipes(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    title = models.CharField(max_length=200)
    image = models.ImageField(
        'Photo',
        upload_to='recipes/',
        blank=True
    )
    text = models.TextField()
    ingredients = models.ForeignKey(
        'Ingredients',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='recipes')
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='tags')
    duration = models.DurationField(
        db_index=True,
        default=timedelta,
        verbose_name='Duration')
    
    class Meta:
        verbose_name_plural = 'Recipes'
        ordering = ['-duration']

    def __str__(self):
        return self.title


class Ingredients(models.Model):
    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=4, decimal_places=1)
    slug = models.SlugField(unique=True)
    units = models.TextField(max_length=20)

    class Meta:
        verbose_name_plural = 'Ingredients'

    def __str__(self):
        return self.title