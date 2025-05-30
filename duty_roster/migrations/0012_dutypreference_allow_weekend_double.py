# Generated by Django 5.1.7 on 2025-04-27 04:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("duty_roster", "0011_dutyassignment_tow_surge_notified"),
    ]

    operations = [
        migrations.AddField(
            model_name="dutypreference",
            name="allow_weekend_double",
            field=models.BooleanField(
                default=False,
                help_text="I'm fine being scheduled both Saturday and Sunday on the same weekend",
            ),
        ),
    ]
