from django.db.models import F
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
import webcolors
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.validators import UniqueValidator

from recipes.models import (
    Ingredient, IngredientRecipes, Recipes,
    Tag, TagsRecipes)
from users.models import User


class Hex2NameColor(serializers.Field):
    """Transforms color tags to names"""
    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        try:
            data = webcolors.hex_to_name(data)
        except ValueError:
            raise serializers.ValidationError(
                'there is no name for this tag')
        return data


class TagsSerializer(serializers.ModelSerializer):
    color = Hex2NameColor()

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color')


class IngredientsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientsRecipesSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ingredient.id')
    amount = serializers.DecimalField(
        required=True, max_digits=5, decimal_places=2,)

    class Meta:
        model = IngredientRecipes
        fields = ('id', 'amount')


class TagsRecipesSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='tag.id')

    class Meta:
        model = TagsRecipes
        fields = ('id')


class RecipesSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username')
    ingredients = IngredientsRecipesSerializer(
        many=True,
        source='ingredientrecipes_set'
    )
    tags = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True
    )

    class Meta:
        model = Recipes
        fields = '__all__'

    def create(self, validated_data):
        """Create new recipe record in Recipe table"""

        # removing ingredients and tags from data to create a simple recipe
        # and then making manipulations with related models
        ingredients = validated_data.pop('ingredientrecipes_set')
        tags = validated_data.pop('tags')
        recipe = Recipes.objects.create(**validated_data)

        # for each ingresient and tag create record in related model
        for ingredient in ingredients:
            current_ingredient = Ingredient.objects.get(
                id=ingredient.get('ingredient').get('id')
            )
            IngredientRecipes.objects.create(
                ingredient=current_ingredient,
                recipe=recipe,
                amount=ingredient.get('amount'))
        for tag in tags:
            current_tag = Tag.objects.get(id=tag)
            TagsRecipes.objects.create(
                tag=current_tag,
                recipe=recipe
            )
        return recipe

    # REVISION NOTE: compare this function with the same part
    # in create method. Most likely it can be merged
    def add_ingredients(self, recipe, ingredients):
        for ingredient in ingredients:
            IngredientRecipes.objects.create(
                ingredient_id=ingredient.get('ingredient').get('id'),
                amount=ingredient.get('amount'),
                recipe=recipe
            )

    def update(self, instance, validated_data):
        """Update recipe"""
        ingredients = validated_data.pop('ingredientrecipes_set')
        tags = validated_data.pop('tags')
        super().update(instance, validated_data)
        instance.ingredients.clear()
        instance.tags.set(tags)
        self.add_ingredients(instance, ingredients)
        instance.save()
        return instance


class ShoppingFavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipes
        fields = ('id', 'name', 'image', 'cooking_time')


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)
        token['username'] = user.username
        return token


class UsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'is_subscribed')


class UserAuthSerializer(UserCreateSerializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta(UserCreateSerializer.Meta):
        fields = (
            'username', 'id', 'email', 'first_name', 'last_name', 'password',
            'is_subscribed',
        )
        extra_kwargs = {'password': {'write_only': True}}
        model = User

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return user.followers.filter(pk=obj.pk).exists()
        return False


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        write_only=False,
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())])
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(
        write_only=True, required=True)
    first_name = serializers.CharField(write_only=False, required=True)
    last_name = serializers.CharField(write_only=False, required=True)

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'password',
            'first_name', 'last_name',)

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
            )
        user.set_password(validated_data['password'])
        user.save()
        return user


class RecipesGetSerializer(serializers.ModelSerializer):
    author = UsersSerializer()
    tags = TagsSerializer(many=True)
    ingredients = serializers.SerializerMethodField()

    class Meta:
        model = Recipes
        fields = (
            'id', 'tags', 'author', 'ingredients',
            'name', 'image', 'text', 'cooking_time',
            'is_favorited', 'is_in_shopping_cart',)

    def get_ingredients(self, obj):
        return obj.ingredients.values(
            'id', 'name', 'measurement_unit',
            amount=F('ingredientrecipe__amount'))
