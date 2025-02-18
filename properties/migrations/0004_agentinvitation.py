# Generated by Django 5.1.1 on 2024-12-20 10:50

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0003_property_favourites'),
        ('users', '0010_newslettersubscription'),
    ]

    operations = [
        migrations.CreateModel(
            name='AgentInvitation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('email', models.EmailField(max_length=254)),
                ('user_type', models.CharField(choices=[('homeowner', 'Homeowner'), ('assistant', 'Assistant')], max_length=10)),
                ('token', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('is_used', models.BooleanField(default=False)),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invitations', to='users.agent')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
