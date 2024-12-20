# Generated by Django 5.1.2 on 2024-12-02 01:17

import django.core.validators
import django.db.models.deletion
from decimal import Decimal
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("elegant_touch_app", "0039_delete_pedidoitem"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="pedidocliente",
            options={
                "ordering": ["-fecha_pedido"],
                "verbose_name": "Pedido de cliente",
                "verbose_name_plural": "Pedidos de clientes",
            },
        ),
        migrations.AddField(
            model_name="pedidocliente",
            name="total",
            field=models.DecimalField(
                decimal_places=2,
                default=Decimal("0.00"),
                max_digits=10,
                verbose_name="Total del pedido",
            ),
        ),
        migrations.AlterField(
            model_name="pedidocliente",
            name="apellido",
            field=models.CharField(max_length=100, verbose_name="Apellido"),
        ),
        migrations.AlterField(
            model_name="pedidocliente",
            name="celular",
            field=models.CharField(
                default=1,
                max_length=15,
                validators=[
                    django.core.validators.RegexValidator(
                        message="El número de celular debe tener 10 dígitos y solo contener números.",
                        regex="^\\d{10}$",
                    )
                ],
                verbose_name="Celular",
            ),
        ),
        migrations.AlterField(
            model_name="pedidocliente",
            name="ciudad",
            field=models.CharField(max_length=100, verbose_name="Ciudad"),
        ),
        migrations.AlterField(
            model_name="pedidocliente",
            name="cliente",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="pedidos",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="pedidocliente",
            name="codigo_postal",
            field=models.CharField(max_length=5, verbose_name="Código postal"),
        ),
        migrations.AlterField(
            model_name="pedidocliente",
            name="comprobante_pago",
            field=models.FileField(
                blank=True,
                null=True,
                upload_to="comprobantes/",
                verbose_name="Comprobante de pago",
            ),
        ),
        migrations.AlterField(
            model_name="pedidocliente",
            name="correo",
            field=models.EmailField(
                default=None, max_length=254, verbose_name="Correo electrónico"
            ),
        ),
        migrations.AlterField(
            model_name="pedidocliente",
            name="direccion_envio",
            field=models.CharField(max_length=255, verbose_name="Dirección de envío"),
        ),
        migrations.AlterField(
            model_name="pedidocliente",
            name="estado",
            field=models.CharField(
                choices=[
                    ("pendiente", "Pendiente"),
                    ("aprobado", "Aprobado"),
                    ("rechazado", "Rechazado"),
                ],
                default="pendiente",
                max_length=10,
                verbose_name="Estado del pedido",
            ),
        ),
        migrations.AlterField(
            model_name="pedidocliente",
            name="fecha_pedido",
            field=models.DateTimeField(
                auto_now_add=True, verbose_name="Fecha del pedido"
            ),
        ),
        migrations.AlterField(
            model_name="pedidocliente",
            name="metodo_pago",
            field=models.CharField(
                choices=[("bbva", "BBVA"), ("nequi", "Nequi")],
                max_length=20,
                verbose_name="Método de pago",
            ),
        ),
        migrations.AlterField(
            model_name="pedidocliente",
            name="nombre",
            field=models.CharField(max_length=100, verbose_name="Nombre"),
        ),
        migrations.CreateModel(
            name="PedidoDetalle",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("cantidad", models.PositiveIntegerField()),
                (
                    "precio_unitario",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                ("subtotal", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "pedido",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="detalles",
                        to="elegant_touch_app.pedidocliente",
                    ),
                ),
                (
                    "producto",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="elegant_touch_app.producto",
                    ),
                ),
            ],
        ),
    ]
