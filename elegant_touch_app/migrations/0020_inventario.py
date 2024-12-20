# Generated by Django 5.0.4 on 2024-11-14 12:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elegant_touch_app', '0019_proveedor_marca_alter_proveedor_apellido_proveedor_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inventario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.TextField()),
                ('precio', models.FloatField()),
                ('stock', models.IntegerField(default=0)),
                ('cantidad_minima', models.IntegerField(default=0)),
                ('cantidad_maxima', models.IntegerField(default=100)),
                ('entradas', models.IntegerField(default=0)),
                ('salidas', models.IntegerField(default=0)),
                ('fecha_actualizacion', models.DateTimeField(auto_now=True)),
                ('ultima_entrada', models.DateTimeField(blank=True, null=True)),
                ('ultima_salida', models.DateTimeField(blank=True, null=True)),
                ('producto', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='inventario', to='elegant_touch_app.producto')),
                ('proveedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inventarios', to='elegant_touch_app.proveedor')),
            ],
        ),
    ]
