# Generated by Django 5.1.7 on 2025-03-26 23:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("members", "0021_airfield"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="flightlog",
            name="field",
        ),
        migrations.AddField(
            model_name="flightlog",
            name="airfield",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="members.airfield",
            ),
        ),
    ]
