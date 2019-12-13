# Generated by Django 2.2.8 on 2019-12-13 15:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wayneapp', '0004_auto_20191213_1555'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='publisher',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='product',
            name='publisher',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]
