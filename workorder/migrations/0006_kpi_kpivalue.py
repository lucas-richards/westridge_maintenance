# Generated by Django 5.0.3 on 2024-08-13 18:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workorder', '0005_rename_due_date_workorder_first_due_date_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='KPI',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='KPIValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField()),
                ('date', models.DateField()),
                ('kpi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workorder.kpi')),
            ],
        ),
    ]
