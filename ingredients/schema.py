from graphene import InputObjectType
import graphene
from graphene_django import DjangoObjectType
from django.shortcuts import get_object_or_404

from .models import Ingredient, Category


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ("id", "name", "ingredients")


class IngredientType(DjangoObjectType):
    class Meta:
        model = Ingredient
        fields = ("id", "name", "notes", "category")


class Query(graphene.ObjectType):
    all_ingredients = graphene.List(IngredientType)
    category_by_name = graphene.Field(CategoryType, name=graphene.String(required=True))
    hello = graphene.String(default_value="Hi")

    @staticmethod
    def resolve_all_ingredients(root, info):
        # We can easily optimize query count in the resolve method
        return Ingredient.objects.select_related("category").all()

    @staticmethod
    def resolve_category_by_name(root, info, name):
        try:
            return Category.objects.get(name=name)
        except Category.DoesNotExist:
            return None


class CategoryInput(InputObjectType):
    id = graphene.ID()
    name = graphene.String()


class IngredientsInput(InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    notes = graphene.String()
    category = graphene.Field(CategoryInput)


class CreateCategory(graphene.Mutation):
    class Arguments:
        input = CategoryInput(required=True)

    ok = graphene.Boolean()
    category = graphene.Field(CategoryType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        category_instance = Category(name=input.name)
        category_instance.save()
        return CreateCategory(ok=ok, category=category_instance)


class UpdateCategory(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String(required=True)

    ok = graphene.Boolean()
    category = graphene.Field(CategoryType)

    @staticmethod
    def mutate(root, info, **kwargs):
        ok = True
        update_category_instance = get_object_or_404(Category, pk=kwargs['id'])
        if update_category_instance:
            update_category_instance.name = kwargs['name']
            update_category_instance.save()
        return UpdateCategory(ok=ok, category=update_category_instance)


class CreateIngredient(graphene.Mutation):
    class Arguments:
        input = IngredientsInput(required=True)

    ok = graphene.Boolean()
    ingredient = graphene.Field(IngredientType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        category_instance = get_object_or_404(Category, id=input.category.id)
        ingredient_instance = Ingredient(name=input.name, notes=input.notes, category=category_instance)
        ingredient_instance.save()
        return CreateIngredient(ok=ok, ingredient=ingredient_instance)


class UpdateIngredient(graphene.Mutation):
    class Arguments:
        input = IngredientsInput(required=True)

    ok = graphene.Boolean()
    ingredient = graphene.Field(IngredientType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        update_ingredient_instance = get_object_or_404(Ingredient, id=input.id)
        update_ingredient_instance.name = input.name
        update_ingredient_instance.notes = input.notes
        update_ingredient_instance.category = get_object_or_404(Category, id=input.category.id)
        update_ingredient_instance.save()
        return UpdateIngredient(ok=ok, ingredient=update_ingredient_instance)


class Mutation(graphene.ObjectType):
    create_category = CreateCategory.Field()
    update_category = UpdateCategory.Field()
    create_ingredient = CreateIngredient.Field()
    update_ingredient = UpdateIngredient.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
