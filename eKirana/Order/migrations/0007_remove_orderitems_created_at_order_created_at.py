# Generated by Django 4.0.2 on 2022-05-29 16:55

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Order', '0006_orderitems_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitems',
            name='created_at',
        ),
        migrations.AddField(
            model_name='order',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
