# Generated by Django 5.1.3 on 2025-02-18 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0007_alter_property_compensation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='compensation',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
