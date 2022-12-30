# Generated by Django 4.0.2 on 2022-05-31 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Shop', '0008_rename_orderid_shop_orderinventory_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop_orderinventory',
            name='status',
            field=models.IntegerField(choices=[(0, 'Pending'), (1, 'Accepted'), (2, 'Completed')], default=(0, 'Pending')),
        ),
    ]
