# Generated by Django 5.0.4 on 2024-11-16 02:24

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elegant_touch_app', '0024_alter_metododepago_nombre_metodo_pago_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('estado', models.CharField(choices=[('pendiente', 'Pendiente'), ('procesando', 'Procesando'), ('enviado', 'Enviado'), ('completado', 'Completado'), ('cancelado', 'Cancelado')], default='pendiente', max_length=20)),
                ('total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('direccion_envio', models.CharField(max_length=255)),
                ('detalles_adicionales', models.TextField(blank=True, null=True)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pedidos', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Pedido',
                'verbose_name_plural': 'Pedidos',
                'ordering': ['-fecha_creacion'],
            },
        ),
    ]
