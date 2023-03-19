from django.contrib import admin

from .models import Recipes, Ingredient, Tag, IngredientRecipes, TagsRecipes


class ingredientrecipes_inline(admin.TabularInline):
    model = IngredientRecipes
    extra = 1


class tagrecipes_inline(admin.TabularInline):
    model = TagsRecipes
    extra = 1


class RecipesAdmin(admin.ModelAdmin):
    inlines = (ingredientrecipes_inline, tagrecipes_inline,)


class IngredientAdmin(admin.ModelAdmin):
    inlines = (ingredientrecipes_inline, )


class TagAdmin(admin.ModelAdmin):
    inlines = (tagrecipes_inline, )


admin.site.register(Ingredient)
admin.site.register(Tag)
admin.site.register(Recipes, RecipesAdmin)
