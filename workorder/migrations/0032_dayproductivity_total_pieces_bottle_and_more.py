# Generated by Django 5.0.3 on 2024-11-19 23:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workorder', '0031_alter_proditem_people_inline_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='dayproductivity',
            name='total_pieces_bottle',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='dayproductivity',
            name='total_pieces_foil',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='dayproductivity',
            name='total_pieces_replenishment',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='dayproductivity',
            name='total_pieces_tube',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
