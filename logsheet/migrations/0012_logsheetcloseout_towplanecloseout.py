# Generated by Django 5.1.7 on 2025-04-02 02:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("logsheet", "0011_alter_logsheetpayment_payment_method"),
    ]

    operations = [
        migrations.CreateModel(
            name="LogsheetCloseout",
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
                ("safety_issues", models.TextField(blank=True)),
                ("equipment_issues", models.TextField(blank=True)),
                ("operations_summary", models.TextField(blank=True)),
                (
                    "logsheet",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="closeout",
                        to="logsheet.logsheet",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TowplaneCloseout",
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
                    "start_tach",
                    models.DecimalField(
                        blank=True, decimal_places=1, max_digits=6, null=True
                    ),
                ),
                (
                    "end_tach",
                    models.DecimalField(
                        blank=True, decimal_places=1, max_digits=6, null=True
                    ),
                ),
                (
                    "fuel_added",
                    models.DecimalField(
                        blank=True, decimal_places=1, max_digits=5, null=True
                    ),
                ),
                ("notes", models.TextField(blank=True)),
                (
                    "logsheet",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="towplane_closeouts",
                        to="logsheet.logsheet",
                    ),
                ),
                (
                    "towplane",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="logsheet.towplane",
                    ),
                ),
            ],
        ),
    ]
