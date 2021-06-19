# Generated by Django 3.2.4 on 2021-06-18 16:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('KitchenWeb', '0004_merge_20210618_0926'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dish',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='Позиция')),
                ('description', models.TextField(max_length=500, verbose_name='Описание')),
                ('image', models.ImageField(blank=True, null=True, upload_to='uploads', verbose_name='Фото')),
                ('base_price', models.IntegerField(verbose_name='Базовая цена')),
                ('extra_price', models.JSONField(blank=True, null=True, verbose_name='Дополнительная цена')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='dish', to='KitchenWeb.category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Позиция',
                'verbose_name_plural': 'Позиции',
                'db_table': 'dishes',
            },
        ),
    ]