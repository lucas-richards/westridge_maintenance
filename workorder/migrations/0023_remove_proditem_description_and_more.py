# Generated by Django 5.0.3 on 2024-11-07 22:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workorder', '0022_remove_proditem_description_proditem_set_up_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='proditem',
            name='produced_in_time',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='proditem',
            name='setup_time',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]