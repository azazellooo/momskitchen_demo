# Generated by Django 3.2.4 on 2021-07-06 12:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0027_remove_usertoken_activated'),
    ]

    operations = [
        migrations.AddField(
            model_name='usertoken',
            name='activated',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='employe',
            name='organization_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='employe_org', to='accounts.organization', verbose_name='Внешний ключ на организацию'),
        ),
    ]
