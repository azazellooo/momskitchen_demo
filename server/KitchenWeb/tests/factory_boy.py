import factory
from KitchenWeb.models import Category, Offering, Dish, Garnish, Additional
import random
from accounts.models import Organization, Employe, UserToken, BalanceChange
from KitchenWeb.models import Supplement
from kitchen5bot.models import TelegramUser, TelegramChat, TelegramState


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category
    category_name = 'test category'
    order = 3


# class TelegramUserFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = TelegramUser
#     telegram_id = random.randint(900000000, 941151633)
#     is_bot = False
#     first_name = 'Test'
#     last_name = 'TelegramUser'
#     username = 'test_tg_user'


# class TelegramChatFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = TelegramChat
#
#
# class TelegramStateFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = TelegramState
#
#     telegram_user = factory.SubFactory(TelegramUserFactory)
#     telegram_chat = factory.SubFactory(TelegramChatFactory)
#

class OrganizationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Organization
    name = "Test Organization"
    payment = "('actual', 'фактический расчет')"
    address = "Bishkek"
    bonus_activation = False
    leave_review = True
    is_active = True


class EmployeeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Employe

    tg_username = "testusername"
    tg_id = '3456789'
    organization_id = factory.SubFactory(OrganizationFactory)
    username = factory.Faker('name')
    is_active = True
    is_admin = True
    # bal_em = factory.RelatedFactoryList(BalanceChangeFactory, size=3)
    total_balance = 10


class BalanceChangeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BalanceChange
    employe = factory.SubFactory(EmployeeFactory)
    type = 'accrual'
    sum_balance = 12
    comment = 'test comment for transaction'


class UserTokenFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserToken

    user = factory.SubFactory(EmployeeFactory)


class SupplementFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Supplement

    name = factory.Faker('name')
    price = random.randint(100, 400)


class DishFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Dish
    name = 'test position'
    description = 'test description'
    category = factory.SubFactory(CategoryFactory)
    base_price = 123
    extra_price = '{"0.5": {"comment": "Comment", "pricing": "25"}}'


class GarnishFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Garnish
    name = 'test garnish'
    order = 2
    base_price = 13


class AdditionalFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Additional
    name = 'test additional'
    sampling_order = 2
    base_price = 123


class OfferingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Offering

    position = factory.SubFactory(DishFactory)
    garnish = factory.SubFactory(GarnishFactory)
    supplement = factory.SubFactory(SupplementFactory)
    additional = factory.SubFactory(AdditionalFactory)
    qty_portion = 5
    date = '2021-07-20'