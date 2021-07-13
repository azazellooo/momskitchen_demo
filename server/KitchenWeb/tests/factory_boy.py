import factory
from KitchenWeb.models import Category
import random

from accounts.models import Organization, Employe, UserToken, BalanceChange
from kitchen5bot.models import TelegramUser, TelegramChat, TelegramState


class CategoryFacroty(factory.Factory):
    class Meta:
        model = Category
    category_name = factory.Faker('name')
    order = str(random.randint(0, 10))


class TelegramChatFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TelegramChat


class TelegramUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TelegramUser
    telegram_id = 941151624
    is_bot = False
    first_name = 'Test'
    last_name = 'TelegramUser'
    username = 'test_tg_user'


class TelegramStateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TelegramState

    telegram_user = factory.SubFactory(TelegramUserFactory)
    telegram_chat = factory.SubFactory(TelegramChatFactory)


class OrganizationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Organization
    pk = 1
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
    username = 'test user'
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



