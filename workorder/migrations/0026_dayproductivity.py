# Generated by Django 5.0.3 on 2024-11-08 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workorder', '0025_proditemstd_setup_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='DayProductivity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('people', models.IntegerField()),
                ('extra_hours', models.FloatField()),
                ('earned_hours', models.FloatField()),
                ('productivity', models.FloatField()),
                ('total_produced', models.IntegerField()),
            ],
        ),
    ]
