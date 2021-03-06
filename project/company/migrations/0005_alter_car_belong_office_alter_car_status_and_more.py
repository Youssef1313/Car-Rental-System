# Generated by Django 4.0 on 2022-01-08 22:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0004_alter_car_is_reserved'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='belong_office',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cars', to='company.office'),
        ),
        migrations.AlterField(
            model_name='car',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='cars', to='company.carstatus'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='car',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reservations', to='company.car'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='reservations', to='company.customer'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='payment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='reservation', to='company.payment', unique=True),
        ),
    ]
