# Generated by Django 3.2.4 on 2021-06-14 06:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_usertoken'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usertoken',
            name='user',
        ),
        migrations.DeleteModel(
            name='Users',
        ),
        migrations.DeleteModel(
            name='UserToken',
        ),
    ]
