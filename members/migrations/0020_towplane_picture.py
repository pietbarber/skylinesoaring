# Generated by Django 5.1.7 on 2025-03-26 23:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("members", "0019_towplane_flightlog"),
    ]

    operations = [
        migrations.AddField(
            model_name="towplane",
            name="picture",
            field=models.ImageField(
                blank=True, null=True, upload_to="towplane_photos/"
            ),
        ),
    ]
