# Generated by Django 5.1.7 on 2025-03-29 04:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("members", "0028_delete_airfield"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="member",
            name="glider_owned",
        ),
        migrations.RemoveField(
            model_name="member",
            name="second_glider_owned",
        ),
    ]
