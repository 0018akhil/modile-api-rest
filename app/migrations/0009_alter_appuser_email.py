# Generated by Django 4.2.4 on 2023-08-12 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_alter_appuser_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appuser',
            name='email',
            field=models.EmailField(default=None, max_length=254, null=True),
        ),
    ]