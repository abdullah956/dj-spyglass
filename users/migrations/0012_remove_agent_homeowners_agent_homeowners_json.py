# Generated by Django 5.1.1 on 2025-02-06 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_remove_agent_homeowner_agent_homeowners'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='agent',
            name='homeowners',
        ),
        migrations.AddField(
            model_name='agent',
            name='homeowners_json',
            field=models.JSONField(blank=True, default=list),
        ),
    ]
