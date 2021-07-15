import factory
from KitchenWeb.models import Category
import random

from accounts.models import Organization, Employe, UserToken, BalanceChange
from KitchenWeb.models import Supplement
from kitchen5bot.models import TelegramUser


class CategoryFacroty(factory.Factory):
    class Meta:
        model = Category
    category_name = factory.Faker('name')
    order = str(random.randint(0, 10))


class TelegramUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TelegramUser
    telegram_id = random.randint(900000000, 941151633)
    is_bot = False
    first_name = 'Test'
    last_name = 'TelegramUser'
    username = 'test_tg_user'


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

    tg_user = factory.SubFactory(TelegramUserFactory)
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


class SuplementFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Supplement

    name = factory.Faker('name')
    price = random.randint(100, 400)



