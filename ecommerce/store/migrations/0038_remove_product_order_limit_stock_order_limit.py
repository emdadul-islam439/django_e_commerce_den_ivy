# Generated by Django 4.1 on 2022-11-20 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0037_rename_buyingitem_purchaseditem_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='order_limit',
        ),
        migrations.AddField(
            model_name='stock',
            name='order_limit',
            field=models.IntegerField(default=50),
        ),
    ]
