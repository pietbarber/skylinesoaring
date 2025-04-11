# Generated by Django 5.1.7 on 2025-04-11 03:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("logsheet", "0022_remove_flight_field"),
    ]

    operations = [
        migrations.AddField(
            model_name="flight",
            name="airfield",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="logsheet.airfield",
            ),
        ),
    ]
