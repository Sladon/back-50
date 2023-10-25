# Generated by Django 4.2.5 on 2023-10-10 15:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ProductosLocales', '0002_producto_descripcion'),
    ]

    operations = [
        migrations.AddField(
            model_name='local',
            name='ubicacion',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='producto',
            name='local',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ProductosLocales.local'),
        ),
    ]