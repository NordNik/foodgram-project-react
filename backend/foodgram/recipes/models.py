from django.db import models

from users.models import User


class Tag(models.Model):
    name = models.CharField(max_length=200)
    color = models.CharField(max_length=200)
    slug = models.SlugField()

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    measurement_unit = models.TextField(max_length=20)

    class Meta:
        verbose_name_plural = 'Ingredients'

    def __str__(self):
        return self.name


class Recipes(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    name = models.CharField(max_length=200)
    image = models.ImageField(
        'Photo',
        upload_to='recipes_photo/'
    )
    text = models.TextField()
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipes',
        related_name='recipes'
    )
    tags = models.ManyToManyField(
        Tag,
        through='TagsRecipes',
        related_name='tags'
    )
    cooking_time = models.IntegerField(verbose_name='Duration')
    shopping_cart = models.ManyToManyField(
        User,
        related_name='shopping_cart',
        verbose_name='shopping_cart',
        blank=True
    )
    is_favorited = models.ManyToManyField(
        User,
        related_name='is_favorite',
        verbose_name='is_favorite',
        blank=True
    )
    date_created = models.DateField('Date created', auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Recipes'
        ordering = ['-date_created']

    def __str__(self):
        return self.name


class IngredientRecipes(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredientrecipe'
    )
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=5, decimal_places=2, blank=True)

    def __str__(self):
        return f'{self.ingredient} {self.recipe} {self.amount}'


class TagsRecipes(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.tag} {self.recipe}'
