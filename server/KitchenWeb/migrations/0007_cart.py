# Generated by Django 3.2.4 on 2021-08-10 14:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_review'),
        ('KitchenWeb', '0006_delete_cart'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.IntegerField(default=1, verbose_name='Кол-во товара')),
                ('portions', models.JSONField(verbose_name='Порции')),
                ('is_confirmed', models.BooleanField(default=False)),
                ('price', models.IntegerField(default=0)),
                ('offering', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_offering', to='KitchenWeb.offering', verbose_name='Предложение')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_user', to='accounts.employee', verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Корзина',
                'verbose_name_plural': 'Корзины',
                'db_table': 'cart',
            },
        ),
    ]
