from django.contrib import admin

from .models import Recipes, Ingredient, Tag, IngredientRecipes, TagsRecipes


class IngredientrecipesInline(admin.TabularInline):
    model = IngredientRecipes
    extra = 1


class TagrecipesInline(admin.TabularInline):
    model = TagsRecipes
    extra = 1


class RecipesAdmin(admin.ModelAdmin):
    inlines = (IngredientrecipesInline, TagrecipesInline,)


class IngredientAdmin(admin.ModelAdmin):
    inlines = (IngredientrecipesInline, )


class TagAdmin(admin.ModelAdmin):
    inlines = (TagrecipesInline, )


admin.site.register(Ingredient)
admin.site.register(Tag)
admin.site.register(Recipes, RecipesAdmin)
