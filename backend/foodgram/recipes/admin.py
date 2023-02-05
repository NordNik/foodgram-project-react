from django.contrib import admin

from .models import Ingredients, Recipes


class RecipesAdmin(admin.ModelAdmin):
    pass
    #list_display = ('pk', 'title', 'text', 'duration')
    #search_fields = ('title', 'text')
    #list_filter = ('duration',)
    #list_editable = ('tags',)
    #empty_value_display = '-empty-'


admin.site.register(Ingredients)
admin.site.register(Recipes, RecipesAdmin)
