# Generated by Django 4.2.4 on 2023-08-12 10:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_alter_spamreport_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='spamreport',
            unique_together={('phone_number', 'reporter')},
        ),
    ]