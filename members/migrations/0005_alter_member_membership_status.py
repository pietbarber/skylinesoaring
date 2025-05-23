# Generated by Django 5.1.7 on 2025-03-24 04:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("members", "0004_member_membership_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="member",
            name="membership_status",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Full Member", "Full Member"),
                    ("Student Member", "Student Member"),
                    ("Family Member", "Family Member"),
                    ("Founding Member", "Founding Member"),
                    ("Honorary Member", "Honorary Member"),
                    ("Emeritus Member", "Emeritus Member"),
                    ("SSEF Member", "SSEF Member"),
                    ("Temporary Member", "Temporary Member"),
                    ("Introductory Member", "Introductory Member"),
                    ("Inactive", "Inactive"),
                    ("Non-Member", "Non-Member"),
                ],
                default="Non-Member",
                max_length=20,
                null=True,
            ),
        ),
    ]
