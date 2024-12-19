# Generated by Django 5.0.3 on 2024-12-19 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workorder', '0038_rename_bottle_productivity_dayproductivity_productivity_bottle_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='proditemstd',
            name='formula',
            field=models.CharField(blank=True, choices=[('glide', 'Glide'), ('silicone A', 'Silicone A'), ('free', 'Free'), ('sanitaizer A', 'Sanitaizer A'), ('t-glide', 'T-Glide')], max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='proditemstd',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
    ]