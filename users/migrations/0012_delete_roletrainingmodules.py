# Generated by Django 5.0.3 on 2024-04-26 23:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_remove_profile_training_events'),
    ]

    operations = [
        migrations.DeleteModel(
            name='RoleTrainingModules',
        ),
    ]