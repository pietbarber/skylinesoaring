# Generated by Django 5.1.7 on 2025-03-26 00:58

import django.db.models.deletion
import members.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("members", "0012_member_towpilot"),
    ]

    operations = [
        migrations.CreateModel(
            name="Biography",
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
                ("content", models.TextField(blank=True, null=True)),
                (
                    "uploaded_image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=members.models.biography_upload_path,
                    ),
                ),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "member",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
