# Generated by Django 5.0.4 on 2024-10-07 13:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elegant_touch_app', '0006_remove_detalleventa_producto_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='producto',
            name='inventario',
        ),
    ]