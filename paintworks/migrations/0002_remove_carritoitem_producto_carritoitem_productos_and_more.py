# Generated by Django 5.1.6 on 2025-03-11 01:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paintworks', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='carritoitem',
            name='producto',
        ),
        migrations.AddField(
            model_name='carritoitem',
            name='productos',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='paintworks.productos'),
        ),
        migrations.DeleteModel(
            name='Datos',
        ),
    ]
