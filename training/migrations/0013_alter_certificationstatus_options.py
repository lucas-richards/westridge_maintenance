# Generated by Django 5.0.3 on 2024-03-28 17:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0012_alter_certificationstatus_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='certificationstatus',
            options={'ordering': ['-completed_date']},
        ),
    ]