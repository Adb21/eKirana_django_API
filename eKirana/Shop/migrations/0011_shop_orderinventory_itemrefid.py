# Generated by Django 4.0.2 on 2022-05-31 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Shop', '0010_alter_shop_orderinventory_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop_orderinventory',
            name='ItemRefID',
            field=models.CharField(default=0, max_length=50),
            preserve_default=False,
        ),
    ]
