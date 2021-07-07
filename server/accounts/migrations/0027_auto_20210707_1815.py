# Generated by Django 3.2.4 on 2021-07-07 18:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0026_alter_employe_organization_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usertoken',
            name='activated',
        ),
        migrations.AlterField(
            model_name='employe',
            name='organization_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.organization', verbose_name='Внешний ключ на организацию'),
        ),
        migrations.CreateModel(
            name='BalanceChange',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('accrual', 'Accrual'), ('write-off', 'Write-off')], max_length=200, verbose_name='Тип')),
                ('sum_balance', models.IntegerField(default=0, verbose_name='Сумма')),
                ('comment', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Комментарий')),
                ('employe', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='bal_em', to='accounts.employe', verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Изменение Баланса',
                'verbose_name_plural': 'Изменение Балансов',
                'db_table': 'BalanceChange',
            },
        ),
    ]
