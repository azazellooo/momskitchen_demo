from django.core.validators import MinValueValidator
from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(models.Model):
    category_name = models.TextField(max_length=30, null=False, blank=False, verbose_name='Category')
    order = models.IntegerField(null=False, blank=False, verbose_name='Category Order', validators=(MinValueValidator(1),))

    class Meta:
        db_table = 'categories'
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.category_name


class Supplement(BaseModel):
    name = models.CharField(max_length=300, blank=False, null=False, verbose_name='Надбавка')
    price = models.PositiveIntegerField(blank=False, null=False, verbose_name='Цена за надбавку')

    class Meta:
        db_table = 'supplements'
        verbose_name = 'Надбавка'
        verbose_name_plural = 'Надбавки'

    def str(self):
        return f'надбавка: {self.name}'

class Dish(models.Model):
    name = models.CharField(max_length=250, blank=False, null=False, verbose_name='Позиция')
    description = models.TextField(max_length=500, blank=False, null=False, verbose_name='Описание')
    category = models.ForeignKey('KitchenWeb.Category', blank=False, null=False, verbose_name='Категория', on_delete=models.PROTECT, related_name='dish')
    image = models.ImageField(blank=True, null=True, upload_to='uploads', verbose_name='Фото')
    base_price = models.IntegerField(blank=False, null=False, verbose_name='Базовая цена')
    extra_price = models.JSONField(blank=True, null=True, verbose_name='Дополнительная цена')

    class Meta:
        db_table = 'dishes'
        verbose_name = 'Позиция'
        verbose_name_plural = 'Позиции'

    def __str__(self):
        return self.name



class Garnish(BaseModel):
    name = models.CharField(max_length=250, blank=False, null=False, verbose_name='Гарнир')
    order = models.IntegerField(null=False, blank=False, verbose_name='Очередность', validators=(MinValueValidator(1),))
    base_price = models.IntegerField(blank=False, null=False, verbose_name='Базовая цена')
    extra_price = models.JSONField(blank=True, null=True, verbose_name='Дополнительная цена')


    class Meta:
        db_table = 'garnishes'
        verbose_name = 'Гарнир'
        verbose_name_plural = 'Гарниры'

    def __str__(self):
        return self.name


class Additional(BaseModel):
    name = models.CharField(max_length=200, blank=False, null=False, verbose_name='Дополнение к позиции')
    sampling_order = models.IntegerField(blank=False, null=False, verbose_name='Очередность при выборке')
    base_price = models.IntegerField(blank=False, null=False, verbose_name='Базовая цена')
    extra_price = models.JSONField(blank=True, null=True, verbose_name='Дополнительная цена')

    class Meta:
        db_table = 'Additional'
        verbose_name = 'Дополнение к позиции'
        verbose_name_plural = 'Дополнения к позициям'

    def __str__(self):
        return self.name


class Offering(BaseModel):
    position = models.OneToOneField('KitchenWeb.Dish', blank=False, null=False, verbose_name='Позиция', on_delete=models.CASCADE, related_name='offering_position')
    garnish = models.ForeignKey('KitchenWeb.Garnish', blank=True, null=True, verbose_name='Гарнир', on_delete=models.SET_NULL, related_name='offering_garnish')
    supplement = models.ForeignKey('KitchenWeb.Supplement', blank=True, null=True, verbose_name='Надбавка', on_delete=models.SET_NULL, related_name='offering_supplement')
    additional = models.ForeignKey('KitchenWeb.Additional', blank=True, null=True, verbose_name='Дополнения', on_delete=models.SET_NULL, related_name='offering_additional')
    qty_portion = models.IntegerField(blank=False, null=False, default=0)
    date = models.DateField(blank=False, null=False, verbose_name='Дата')

    class Meta:
        db_table = 'offerings'
        verbose_name = 'Предложение по позиции'
        verbose_name_plural = 'Предложения по позициям'

    def __str__(self):
        return f'{self.position}-{self.date}'
