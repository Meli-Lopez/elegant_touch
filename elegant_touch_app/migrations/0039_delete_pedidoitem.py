# Generated by Django 5.0.4 on 2024-12-01 17:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elegant_touch_app', '0038_remove_pedidocliente_total'),
    ]

    operations = [
        migrations.DeleteModel(
            name='PedidoItem',
        ),
    ]
