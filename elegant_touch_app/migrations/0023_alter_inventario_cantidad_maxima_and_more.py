# Generated by Django 5.0.4 on 2024-11-15 01:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elegant_touch_app', '0022_inventario_agotado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventario',
            name='cantidad_maxima',
            field=models.IntegerField(default=1000),
        ),
        migrations.AlterField(
            model_name='inventario',
            name='cantidad_minima',
            field=models.IntegerField(default=10),
        ),
    ]
