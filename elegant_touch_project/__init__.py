# Crea una migración para agregar un campo nullable
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('elegant_touch_app', 'nombre_migracion_anterior'),  # Reemplaza con el nombre de la migración anterior
    ]

    operations = [
        migrations.AddField(
            model_name='categoria',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID', null=True),
        ),
    ]
