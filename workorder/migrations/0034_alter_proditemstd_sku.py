# Generated by Django 5.0.3 on 2024-11-21 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workorder', '0033_proditemstd_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proditemstd',
            name='sku',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
