# Generated by Django 5.1.1 on 2024-09-10 09:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_user_options_alter_user_groups_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='subscription_status',
        ),
    ]
