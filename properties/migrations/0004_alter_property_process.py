# Generated by Django 5.1.1 on 2024-09-11 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0003_alter_connectionrequest_receiver_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='process',
            field=models.CharField(choices=[('%', 'Percentage'), ('$', 'Dollar'), ('Contact Agent', 'Contact Agent'), ('Send Offer', 'Send Offer')], max_length=15),
        ),
    ]