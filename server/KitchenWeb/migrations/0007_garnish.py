# Generated by Django 3.2.4 on 2021-06-22 09:44

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('KitchenWeb', '0006_auto_20210618_1628'),
    ]

    operations = [
        migrations.CreateModel(
            name='Garnish',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=250, verbose_name='Гарнир')),
                ('order', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Очередность')),
                ('base_price', models.IntegerField(verbose_name='Базовая цена')),
                ('extra_price', models.JSONField(blank=True, null=True, verbose_name='Дополнительная цена')),
            ],
            options={
                'verbose_name': 'Гарнир',
                'verbose_name_plural': 'Гарниры',
                'db_table': 'garnishes',
            },
        ),
    ]