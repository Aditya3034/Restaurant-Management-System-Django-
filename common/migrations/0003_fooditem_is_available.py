# Generated by Django 5.1.1 on 2024-10-20 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_remove_fooditem_is_available'),
    ]

    operations = [
        migrations.AddField(
            model_name='fooditem',
            name='is_available',
            field=models.BooleanField(default=True),
        ),
    ]
