# Generated by Django 5.1.4 on 2024-12-31 17:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cheque',
            name='payment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cheques', to='app1.paymnet'),
        ),
    ]
