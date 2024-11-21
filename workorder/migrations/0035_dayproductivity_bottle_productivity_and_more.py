# Generated by Django 5.0.3 on 2024-11-21 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workorder', '0034_alter_proditemstd_sku'),
    ]

    operations = [
        migrations.AddField(
            model_name='dayproductivity',
            name='bottle_productivity',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='dayproductivity',
            name='foil_productivity',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='dayproductivity',
            name='replenishment_productivity',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='dayproductivity',
            name='tube_productivity',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
