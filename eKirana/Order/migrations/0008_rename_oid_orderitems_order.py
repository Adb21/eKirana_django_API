# Generated by Django 4.0.2 on 2022-05-30 04:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Order', '0007_remove_orderitems_created_at_order_created_at'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderitems',
            old_name='oid',
            new_name='Order',
        ),
    ]