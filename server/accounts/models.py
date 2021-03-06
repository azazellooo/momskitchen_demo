from django.db import models
from django.core.validators import MinLengthValidator, MinValueValidator
import uuid
from bot.telegram_bot import TelegramBot
from django.db.models.signals import post_save
from django.dispatch import receiver

BASE_URL = 'http://t.me/MommyKitchenbot/'

choice_types = [('accrual', 'Начисление'), ('write-off', 'Списание')]


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


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


class Employee(models.Model):
    tg_username = models.CharField(max_length=128, null=True, blank=True, verbose_name='Юзернейм телеграм юзера')
    tg_id = models.CharField(max_length=128, null=False, blank=False, verbose_name='ID телеграм юзера')
    tg_firstname = models.CharField(max_length=128, null=True, blank=True, verbose_name='Имя телеграм юзера')
    tg_lastname = models.CharField(max_length=128, null=True, blank=True, verbose_name='Фамилия телеграм юзера')
    organization_id = models.ForeignKey('accounts.Organization', on_delete=models.CASCADE,
                                        blank=False, null=False, related_name='employe_org', verbose_name='Внешний ключ на организацию')
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
        if self.tg_username:
            return self.tg_username
        return self.tg_id


class BalanceChange(models.Model):
    type = models.CharField(max_length=200, choices=choice_types, blank=False, null=False, verbose_name='Тип')
    employee = models.ForeignKey('accounts.Employee', on_delete=models.CASCADE, related_name='bal_em', verbose_name='Пользователь')
    sum_balance = models.IntegerField(default=0, blank=False, null=False, verbose_name='Сумма', validators=[MinValueValidator(1)])
    comment = models.CharField(max_length=1000, blank=True, null=True, verbose_name='Комментарий')
    created_at = models.DateTimeField(auto_now_add=True)
    balance_after_transaction = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'BalanceChange'
        verbose_name = 'Изменение Баланса'
        verbose_name_plural = 'Изменение Балансов'


@receiver(post_save, sender=BalanceChange)
def send_notification(sender, instance, created, **kwargs):
    transaction = instance
    employee = transaction.employee
    chat_user_id = employee.tg_id
    bot = TelegramBot()
    if created:
        if transaction.type == 'accrual':
            current_balance = employee.total_balance + int(transaction.sum_balance)
            message = f'на ваш баланс было начислено {transaction.sum_balance} сомов. Ваш текущий баланс: {current_balance} сомов.Комментарий к транзакции: {transaction.comment}'
            bot.send_message(recipient=chat_user_id, message=message, parse_mode=None)
        else:
            current_balance = employee.total_balance - int(transaction.sum_balance)
            message = f'С Вашего баланса было списано {transaction.sum_balance} сомов. Ваш текущий баланс: {current_balance} сомов.Комментарий к транзакции: {transaction.comment}'
            bot.send_message(recipient=chat_user_id, message=message)


class Review(BaseModel):
    user_name = models.ForeignKey('accounts.Employee', on_delete=models.CASCADE, related_name='review_name', verbose_name='имя пользователя')
    text_review = models.TextField(max_length=500, blank=False, null=False, verbose_name='текст отзыва')

    class Meta:
        db_table = 'Reviews'
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'



class UserToken(models.Model):
    key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True)
    user = models.OneToOneField('accounts.Employee', on_delete=models.CASCADE, related_name='user_token')
    created_at = models.DateTimeField(auto_now_add=True)
    activated = models.BooleanField(default=False)

    class Meta:
        db_table = 'UserTokens'
        verbose_name = 'Токен пользователя'
        verbose_name_plural = 'Токены Пользователей'



