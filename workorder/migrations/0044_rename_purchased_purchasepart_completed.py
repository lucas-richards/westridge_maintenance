# Generated by Django 5.1.5 on 2025-03-07 20:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workorder', '0043_delete_completeditem'),
    ]

    operations = [
        migrations.RenameField(
            model_name='purchasepart',
            old_name='purchased',
            new_name='completed',
        ),
    ]
