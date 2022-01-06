# Generated by Django 4.0 on 2022-01-06 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0002_auto_20220105_1049'),
    ]

    operations = [
        migrations.RenameField(
            model_name='office',
            old_name='office_id',
            new_name='id',
        ),
        migrations.RenameField(
            model_name='payment',
            old_name='payment_id',
            new_name='id',
        ),
        migrations.RenameField(
            model_name='reservation',
            old_name='reservation_id',
            new_name='id',
        ),
        migrations.AlterField(
            model_name='car',
            name='model',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='office',
            name='office_location',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='office',
            name='office_name',
            field=models.CharField(max_length=256),
        ),
    ]
