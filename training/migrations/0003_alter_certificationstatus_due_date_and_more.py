# Generated by Django 4.1.7 on 2024-03-16 19:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certificationstatus',
            name='due_date',
            field=models.DateField(blank=True, default=datetime.datetime(2024, 3, 31, 19, 11, 53, 8149, tzinfo=datetime.timezone.utc), null=True),
        ),
        migrations.AlterField(
            model_name='certificationstatus',
            name='scheduled_date',
            field=models.DateField(blank=True, default=datetime.datetime(2024, 3, 31, 19, 11, 53, 6730, tzinfo=datetime.timezone.utc), null=True),
        ),
    ]
