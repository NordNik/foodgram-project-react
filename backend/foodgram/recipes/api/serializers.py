from rest_framework import serializers
import webcolors

from recipes.models import Recipes, Tag


class RecipesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipes
        fields = '__all__'


class Hex2NameColor(serializers.Field):
    def to_representation(self, value):
        return value
    def to_internal_value(self, data):
        try:
            data = webcolors.hex_to_name(data)
        except ValueError:
            raise serializers.ValidationError('there is no name for this tag')
        return data


class TagsSerializer(serializers.ModelSerializer):
    color = Hex2NameColor()

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')
