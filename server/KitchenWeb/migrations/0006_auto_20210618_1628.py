# Generated by Django 3.2.4 on 2021-06-18 16:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('KitchenWeb', '0005_dish'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='supplement',
            options={'verbose_name': 'Надбавка', 'verbose_name_plural': 'Надбавки'},
        ),
        migrations.AlterModelTable(
            name='supplement',
            table='supplements',
        ),
    ]