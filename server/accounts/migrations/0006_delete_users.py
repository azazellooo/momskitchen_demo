# Generated by Django 3.2.4 on 2021-06-12 07:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_delete_usertoken'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Users',
        ),
    ]
