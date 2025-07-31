from apps.categories.entity import Category
from apps.categories.schema import CategoryNestedSchema, CategorySchema
from apps.categories.models import CategoryModel
from apps.shared.value_objects import Name, Description


def category_to_schema(category: Category) -> CategorySchema:
    return CategorySchema(
        id=category.id,
        name=category.name.value,
        description=category.description.value,
        created_at=category.created_at,
        updated_at=category.updated_at,
    )


def category_to_nested_schema(category: Category) -> CategoryNestedSchema:
    return CategoryNestedSchema(
            id=category.id,
            name=category.name.value,
            description=category.description.value,
        )

def category_model_to_entity(category_model: CategoryModel) -> Category:
    return Category(Name(category_model.name), Description(category_model.description), category_model.id)
