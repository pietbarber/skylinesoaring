# Generated by Django 5.1.7 on 2025-04-14 23:57

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("logsheet", "0023_flight_airfield"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="glider",
            name="is_active",
            field=models.BooleanField(
                default=True,
                help_text="Uncheck to hide this glider from flight entry dropdowns",
            ),
        ),
        migrations.AddField(
            model_name="glider",
            name="owners",
            field=models.ManyToManyField(
                blank=True,
                help_text="Members who own this glider",
                related_name="gliders_owned",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
