# Generated by Django 4.1 on 2022-09-10 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0020_alter_order_date_completed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='image',
            field=models.ImageField(default='default.png', upload_to='profile_pics'),
        ),
    ]