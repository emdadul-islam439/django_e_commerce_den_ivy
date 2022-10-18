# Generated by Django 4.1 on 2022-10-07 01:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0024_rename_order_cart_rename_order_cartitem_cart_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_status', models.IntegerField(choices=[(0, 'Waiting Payment'), (1, 'Payment Received'), (2, 'Preparing'), (3, 'Prepared'), (4, 'Shipping'), (5, 'Delivered'), (6, 'Cancelled')], default=0, verbose_name='Order Status')),
                ('payment_option', models.CharField(choices=[('Cash On Delivery', 'Cash On Delivery'), ('Bkash', 'Bkash')], default='Cash On Delivery', max_length=20, verbose_name='Payment Options')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created in')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modified in')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.customer')),
            ],
            options={
                'verbose_name': 'Order',
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(blank=True, default=0, null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.order')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.product')),
            ],
        ),
    ]