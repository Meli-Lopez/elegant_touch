# Generated by Django 5.0.4 on 2024-10-03 14:34

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elegant_touch_app', '0004_alter_detalle_cantidad_detalle_pedido'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categoria',
            name='nombre_categoria',
        ),
        migrations.AddField(
            model_name='categoria',
            name='nombre',
            field=models.CharField(default='null', max_length=100),
        ),
        migrations.CreateModel(
            name='Subcategoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subcategorias', to='elegant_touch_app.categoria')),
            ],
        ),
        migrations.CreateModel(
            name='GestionCategoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_actualizacion', models.DateTimeField(auto_now=True)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elegant_touch_app.categoria')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('subcategoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elegant_touch_app.subcategoria')),
            ],
            options={
                'verbose_name': 'Gestión de Categoría',
                'verbose_name_plural': 'Gestiones de Categorías',
            },
        ),
    ]
