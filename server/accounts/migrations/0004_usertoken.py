# Generated by Django 3.2.4 on 2021-06-12 07:11

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_users_username'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_token', to='accounts.users')),
            ],
            options={
                'verbose_name': 'Токен пользователя',
                'verbose_name_plural': 'Токены Пользователей',
                'db_table': 'UserTokens',
            },
        ),
    ]

