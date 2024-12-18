# Generated by Django 5.1.1 on 2024-10-20 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0005_rename_order_date_order_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery_status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Out for Delivery', 'Out for Delivery'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled')], default='Pending', max_length=20),
        ),
    ]
