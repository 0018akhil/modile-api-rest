# Generated by Django 4.2.4 on 2023-08-12 08:17

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_remove_appuser_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='appuser',
            name='name',
            field=models.CharField(default=django.utils.timezone.now, max_length=100),
            preserve_default=False,
        ),
    ]
