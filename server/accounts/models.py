from django.db import models
# Create your models here.
import uuid


class Organization(models.Model):
    name = models.CharField(max_length=300, blank=False, null=False)
    secondary_key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        db_table = 'Organization'
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'

    def __str__(self):
        return self.name

class Users(models.Model):
    tg_user = models.OneToOneField('kitchen5bot.TelegramUser', on_delete = models.CASCADE)
    organization_id = models.ForeignKey('accounts.Organization', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = 'Users'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
