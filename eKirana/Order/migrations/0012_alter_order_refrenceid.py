# Generated by Django 4.0.2 on 2022-05-31 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Order', '0011_alter_order_status_alter_orderitems_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='RefrenceID',
            field=models.CharField(max_length=30),
        ),
    ]