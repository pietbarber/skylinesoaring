# Generated by Django 5.1.7 on 2025-04-01 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("logsheet", "0006_flight_split_type_flight_split_with"),
    ]

    operations = [
        migrations.AlterField(
            model_name="flight",
            name="split_type",
            field=models.CharField(
                blank=True,
                choices=[
                    ("even", "50/50"),
                    ("tow", "Tow Only"),
                    ("rental", "Rental Only"),
                    ("full", "Full Cost"),
                ],
                max_length=10,
                null=True,
            ),
        ),
    ]
