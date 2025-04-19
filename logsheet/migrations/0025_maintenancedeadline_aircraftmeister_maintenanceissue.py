# Generated by Django 5.1.7 on 2025-04-19 17:07

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("logsheet", "0024_glider_is_active_glider_owners"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="MaintenanceDeadline",
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
                    "aircraft_type",
                    models.CharField(
                        choices=[("glider", "Glider"), ("towplane", "Towplane")],
                        max_length=8,
                    ),
                ),
                ("aircraft_n_number", models.CharField(max_length=10)),
                ("item", models.CharField(max_length=100)),
                ("due_date", models.DateField()),
                ("notes", models.TextField(blank=True)),
            ],
            options={
                "ordering": ["due_date"],
            },
        ),
        migrations.CreateModel(
            name="AircraftMeister",
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
                    "aircraft_type",
                    models.CharField(
                        choices=[("glider", "Glider"), ("towplane", "Towplane")],
                        max_length=8,
                    ),
                ),
                ("aircraft_n_number", models.CharField(max_length=10)),
                (
                    "member",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="MaintenanceIssue",
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
                    "aircraft_type",
                    models.CharField(
                        choices=[("glider", "Glider"), ("towplane", "Towplane")],
                        max_length=8,
                    ),
                ),
                ("aircraft_n_number", models.CharField(max_length=10)),
                ("report_date", models.DateField(auto_now_add=True)),
                ("description", models.TextField()),
                ("grounded", models.BooleanField(default=False)),
                ("resolved", models.BooleanField(default=False)),
                ("resolution_notes", models.TextField(blank=True)),
                ("resolved_date", models.DateField(blank=True, null=True)),
                (
                    "reported_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "resolved_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="resolved_maintenance",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-report_date"],
            },
        ),
    ]
