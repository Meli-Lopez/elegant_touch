# Generated by Django 5.0.7 on 2024-11-28 15:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elegant_touch_app', '0029_pedidocliente_pedidoadministrador'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='pedidocliente',
            old_name='fecha_creacion',
            new_name='fecha_pedido',
        ),
        migrations.AlterField(
            model_name='pedidocliente',
            name='cliente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pedidos', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='pedidocliente',
            name='codigo_postal',
            field=models.CharField(max_length=5),
        ),
        migrations.AlterField(
            model_name='pedidocliente',
            name='comprobante_pago',
            field=models.FileField(default=1, upload_to='comprobantes/'),
            preserve_default=False,
        ),
    ]
