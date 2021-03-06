# Generated by Django 3.2.4 on 2021-08-19 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('KitchenWeb', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='additional',
            name='base_price',
            field=models.PositiveIntegerField(verbose_name='Базовая цена'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='price',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='dish',
            name='base_price',
            field=models.PositiveIntegerField(verbose_name='Базовая цена'),
        ),
        migrations.AlterField(
            model_name='garnish',
            name='base_price',
            field=models.PositiveIntegerField(verbose_name='Базовая цена'),
        ),
        migrations.AlterField(
            model_name='orderoffernig',
            name='price',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
