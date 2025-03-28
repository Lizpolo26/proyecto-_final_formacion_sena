# Generated by Django 5.1.6 on 2025-03-11 11:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paintworks', '0002_remove_carritoitem_producto_carritoitem_productos_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='carritoitem',
            name='productos',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='paintworks.productos'),
        ),
        migrations.CreateModel(
            name='Datos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('otro_campo', models.CharField(max_length=100)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
