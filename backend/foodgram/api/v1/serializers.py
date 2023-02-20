from rest_framework import serializers
import webcolors
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.validators import UniqueValidator

from recipes.models import (
    Ingredient, IngredientRecipes, Recipes,
    Tag, TagsRecipes)
from users.models import User


class Hex2NameColor(serializers.Field):
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
        # ## !!!validate tags and ingredients before creating recipe!!! ###
        ingredients = validated_data.pop('ingredientrecipes_set')
        tags = validated_data.pop('tags')
        recipe = Recipes.objects.create(**validated_data)
        for ingredient in ingredients:
            current_ingredient = Ingredient.objects.get(
                id=ingredient['ingredient']['id']
            )
            IngredientRecipes.objects.create(
                ingredient=current_ingredient,
                recipe=recipe,
                amount=ingredient['amount'])
        for tag in tags:
            current_tag = Tag.objects.get(
                id=tag
            )
            TagsRecipes.objects.create(
                tag=current_tag,
                recipe=recipe
            )
        return recipe


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
    tags = serializers.SerializerMethodField()

    class Meta:
        model = Recipes
        fields = (
            'id', 'tags', 'author', 'ingredients',
            'name', 'image', 'text', 'cooking_time')
        # 'is_favorited', 'is_in_shopping_cart',

    def get_tags(self, obj):
        _tags = obj.tags.all()
        print(_tags)
        return TagsRecipesSerializer(
            _tags, many=True, context=self.context
        ).data
