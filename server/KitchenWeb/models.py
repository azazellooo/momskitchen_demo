from django.core.validators import MinValueValidator
from django.db import models


class Category(models.Model):
    category_name = models.TextField(max_length=30, null=False, blank=False, verbose_name='Category')
    order = models.IntegerField(null=False, blank=False, verbose_name='Category Order', validators=(MinValueValidator(1),))

    class Meta:
        db_table = 'categories'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return f'Catgory: {self.category_name}, order: {self.order}'


class Supplement(models.Model):
    name = models.CharField(max_length=300, blank=False, null=False, verbose_name='Надбавка')
    price = models.PositiveIntegerField(blank=False, null=False, verbose_name='Цена за надбавку')

    def str(self):
        return f'надбавка: {self.name}'
