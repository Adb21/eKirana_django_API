# Generated by Django 4.0.2 on 2022-05-31 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Order', '0013_orderitems_itemrefid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitems',
            name='ItemRefID',
            field=models.CharField(max_length=50),
        ),
    ]
