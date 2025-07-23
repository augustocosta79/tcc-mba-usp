from apps.categories.schema import CategoryNestedSchema

def build_category_nested_schema_list(categories: list) -> list[CategoryNestedSchema]:
    return [
        CategoryNestedSchema(
            id=category.id,
            name=category.name,
            description=category.description,
        )
        for category in categories
    ]
