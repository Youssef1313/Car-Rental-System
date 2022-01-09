# Generated by Django 4.0 on 2022-01-09 05:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0005_alter_car_belong_office_alter_car_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='payment',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='reservation', to='company.payment'),
        ),
    ]
