# Generated by Django 4.0 on 2022-01-09 15:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0006_alter_reservation_payment'),
    ]

    operations = [
        migrations.CreateModel(
            name='CarStatusChangeLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.DateField()),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.car')),
                ('new_status', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='company.carstatus')),
            ],
        ),
    ]
