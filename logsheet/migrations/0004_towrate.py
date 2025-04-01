# Generated by Django 5.1.7 on 2025-04-01 00:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("logsheet", "0003_flight_passenger_flight_passenger_name_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="TowRate",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "altitude",
                    models.PositiveIntegerField(
                        help_text="Release altitude in feet (e.g. 2000)"
                    ),
                ),
                (
                    "price",
                    models.DecimalField(
                        decimal_places=2, help_text="Price in USD", max_digits=6
                    ),
                ),
            ],
            options={
                "ordering": ["altitude"],
            },
        ),
    ]
