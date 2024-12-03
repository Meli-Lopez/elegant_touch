# Generated by Django 5.0.4 on 2024-12-01 14:05

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elegant_touch_app', '0032_delete_pedidocliente'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PedidoCliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('apellido', models.CharField(max_length=100)),
                ('celular', models.CharField(blank=True, max_length=15, null=True, validators=[django.core.validators.RegexValidator(message='El número de celular debe tener 10 dígitos y solo contener números.', regex='^\\d{10}$')])),
                ('correo', models.EmailField(blank=True, max_length=254, null=True)),
                ('direccion_envio', models.CharField(max_length=255)),
                ('ciudad', models.CharField(max_length=100)),
                ('codigo_postal', models.CharField(max_length=5)),
                ('metodo_pago', models.CharField(choices=[('bbva', 'BBVA'), ('nequi', 'Nequi')], max_length=20)),
                ('comprobante_pago', models.FileField(blank=True, null=True, upload_to='comprobantes/')),
                ('estado', models.CharField(choices=[('pendiente', 'Pendiente'), ('aprobado', 'Aprobado'), ('rechazado', 'Rechazado')], default='pendiente', max_length=10)),
                ('fecha_pedido', models.DateTimeField(auto_now_add=True)),
                ('cliente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pedidos', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]