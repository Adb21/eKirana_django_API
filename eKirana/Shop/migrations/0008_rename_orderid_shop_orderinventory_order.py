# Generated by Django 4.0.2 on 2022-05-30 04:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Shop', '0007_remove_shop_orderinventory_shoporder_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shop_orderinventory',
            old_name='OrderID',
            new_name='Order',
        ),
    ]
