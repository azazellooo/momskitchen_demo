import factory
from KitchenWeb.models import Category
import random

class CategoryFacroty(factory.Factory):
    class Meta:
        model = Category
    category_name = factory.Faker('name')
    order = str(random.randint(0, 10))
