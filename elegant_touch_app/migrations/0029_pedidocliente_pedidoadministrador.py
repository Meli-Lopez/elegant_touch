# Generated by Django 5.0.7 on 2024-11-28 14:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elegant_touch_app', '0028_remove_pedido_cliente_delete_detallepedido_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PedidoCliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('apellido', models.CharField(max_length=100)),
                ('direccion_envio', models.CharField(max_length=255)),
                ('ciudad', models.CharField(max_length=100)),
                ('codigo_postal', models.CharField(max_length=10)),
                ('comprobante_pago', models.ImageField(blank=True, null=True, upload_to='comprobantes/')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pedidos', to='elegant_touch_app.perfilusuario')),
            ],
        ),
        migrations.CreateModel(
            name='PedidoAdministrador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.CharField(choices=[('pendiente', 'Pendiente'), ('aceptado', 'Aceptado'), ('rechazado', 'Rechazado')], default='pendiente', max_length=20)),
                ('observaciones', models.TextField(blank=True, null=True)),
                ('fecha_revision', models.DateTimeField(auto_now=True)),
                ('pedido_cliente', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='admin_pedido', to='elegant_touch_app.pedidocliente')),
            ],
        ),
    ]
