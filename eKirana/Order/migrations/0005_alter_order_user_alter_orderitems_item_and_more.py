# Generated by Django 4.0.2 on 2022-05-29 08:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Shop', '0005_shop_order_shop_orderinventory'),
        ('Product', '0005_alter_product_image'),
        ('Order', '0004_order_orderitems'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='User',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='orderitems',
            name='Item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Product.product'),
        ),
        migrations.AlterField(
            model_name='orderitems',
            name='Seller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Shop.shopkeeper'),
        ),
        migrations.AlterField(
            model_name='orderitems',
            name='oid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Order.order'),
        ),
    ]
