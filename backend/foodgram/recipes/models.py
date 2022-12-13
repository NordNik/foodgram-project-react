from datetime import timedelta
from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


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
    tags = models.ForeignKey(
        'Tags',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='recipes')
    duration = models.DurationField(
        db_index=True,
        default=timedelta,
        verbose_name='Duration')
    
    class Meta:
        verbose_name_plural = 'Recipes'
        ordering = ['-duration']

    def __str__(self):
        return self.title


class Tags(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    class Meta:
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.title


class Ingredients(models.Model):
    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=4, decimal_places=1)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    class Meta:
        verbose_name_plural = 'Ingredients'

    def __str__(self):
        return self.title