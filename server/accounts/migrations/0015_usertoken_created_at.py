# Generated by Django 3.2.4 on 2021-06-19 18:33

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_auto_20210619_1351'),
    ]

    operations = [
        migrations.AddField(
            model_name='usertoken',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]