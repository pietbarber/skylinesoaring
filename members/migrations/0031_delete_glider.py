# Generated by Django 5.1.7 on 2025-03-29 04:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("members", "0030_member_glider_owned_member_second_glider_owned"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Glider",
        ),
    ]
