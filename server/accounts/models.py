from django.db import models
from django.core.validators import MinLengthValidator, MinValueValidator
import uuid

BASE_URL = 'http://t.me/kitchen5bot/'

choice_types = [('accrual', 'Начисление'), ('write-off', 'Списание')]


class Organization(models.Model):
    PAYMENT_TYPES = [('actual', 'фактический расчет'), ('cumulative', 'накопительный расчет')]
    name = models.CharField(max_length=300, blank=False, null=False, verbose_name='Название компании')
    secondary_key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True,
                                     db_index=True, verbose_name='Вторичный ключ(UUID)')
    payment = models.CharField(max_length=400, choices=PAYMENT_TYPES,
                               default=PAYMENT_TYPES[0], verbose_name='Тип расчета')
    address = models.CharField(max_length=400, blank=False, null=False,
                               default='Bishkek', verbose_name='Адрес компании')
    bonus_activation = models.BooleanField(default=False, verbose_name='Возможность активирования бонуса')
    leave_review = models.BooleanField(default=True, verbose_name='Возможность оставлять отзывы')
    is_active = models.BooleanField(default=True, verbose_name='Активна ли компания')

    class Meta:
        db_table = 'Organization'
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'

    @property
    def generate_link(self):
        return f'{BASE_URL}?start={self.secondary_key}'

    def __str__(self):
        return self.name

class Employe(models.Model):
    tg_user = models.OneToOneField('kitchen5bot.TelegramUser',
                                   on_delete=models.CASCADE, verbose_name='Пользователь телеграма')
    organization_id = models.ForeignKey('accounts.Organization', on_delete=models.CASCADE,
                                        null=True, related_name='employe_org', blank=True, verbose_name='Внешний ключ на организацию')
    username = models.CharField(max_length=200, null=True, blank=True,
                                unique=True, validators=[MinLengthValidator(3)], verbose_name='Username')
    is_active = models.BooleanField(default=True, verbose_name='Активен ли пользователь')
    is_admin = models.BooleanField(default=False)
    total_balance = models.IntegerField(default=0, blank=True, null=True, verbose_name='Общий баланс')

    class Meta:
        db_table = 'Users'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class BalanceChange(models.Model):
    type = models.CharField(max_length=200, choices=choice_types, blank=False, null=False, verbose_name='Тип')
    employe = models.ForeignKey('accounts.Employe', on_delete=models.CASCADE, related_name='bal_em', verbose_name='Пользователь')
    sum_balance = models.IntegerField(default=0, blank=False, null=False, verbose_name='Сумма', validators=[MinValueValidator(1)])
    comment = models.CharField(max_length=1000, blank=True, null=True, verbose_name='Комментарий')
    created_at = models.DateTimeField(auto_now_add=True)
    balance_after_transaction = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'BalanceChange'
        verbose_name = 'Изменение Баланса'
        verbose_name_plural = 'Изменение Балансов'


class UserToken(models.Model):
    key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True)
    user = models.OneToOneField('accounts.Employe', on_delete=models.CASCADE, related_name='user_token')
    created_at = models.DateTimeField(auto_now_add=True)
    activated = models.BooleanField(default=False)

    class Meta:
        db_table = 'UserTokens'
        verbose_name = 'Токен пользователя'
        verbose_name_plural = 'Токены Пользователей'

