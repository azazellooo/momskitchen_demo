# Generated by Django 3.2.4 on 2021-07-10 06:40

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0034_employe_total_balance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='balancechange',
            name='sum_balance',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Сумма'),
        ),
    ]