# Generated by Django 5.0.4 on 2024-12-01 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elegant_touch_app', '0035_alter_pedidoitem_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedidocliente',
            name='total',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]