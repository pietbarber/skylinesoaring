# Generated by Django 5.1.7 on 2025-04-06 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "logsheet",
            "0018_flight_guest_instructor_name_flight_guest_pilot_name_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="flight",
            name="legacy_instructor_name",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="flight",
            name="legacy_passenger_name",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="flight",
            name="legacy_pilot_name",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="flight",
            name="legacy_towpilot_name",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
