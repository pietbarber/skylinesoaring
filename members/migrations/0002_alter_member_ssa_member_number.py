# Generated by Django 5.1.7 on 2025-03-23 23:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("members", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="member",
            name="SSA_member_number",
            field=models.CharField(blank=True, max_length=20, null=True, unique=True),
        ),
    ]
