from django.db import models
from django.core.validators import MinLengthValidator
import uuid

BASE_URL = 'http://t.me/kitchen5bot/'


class Organization(models.Model):
    PAYMENT_TYPES = [('actual', 'фактический расчет'), ('cumulative', 'накопительный расчет')]
    name = models.CharField(max_length=300, blank=False, null=False)
    secondary_key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True)
    payment = models.CharField(max_length=400, choices=PAYMENT_TYPES, default=PAYMENT_TYPES[0])
    address = models.CharField(max_length=400, blank=False, null=False, default='Bishkek')
    bonus_activation = models.BooleanField(default=False)
    leave_review = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'Organization'
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'

    @property
    def generate_link(self):
        return f'{BASE_URL}?start={self.secondary_key}'

    def __str__(self):
        return self.name


class Users(models.Model):
    tg_user = models.OneToOneField('kitchen5bot.TelegramUser', on_delete = models.CASCADE)
    organization_id = models.ForeignKey('accounts.Organization', on_delete=models.CASCADE, null=True, blank=True)
    username = models.CharField(max_length=200, null=True, blank=True, unique=True, validators=[MinLengthValidator(3)])
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'Users'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class UserToken(models.Model):
    key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True)
    user = models.OneToOneField('accounts.Users', on_delete=models.CASCADE, related_name='user_token')

    class Meta:
        db_table = 'UserTokens'
        verbose_name = 'Токен пользователя'
        verbose_name_plural = 'Токены Пользователей'
