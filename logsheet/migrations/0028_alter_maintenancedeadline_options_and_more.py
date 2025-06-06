# Generated by Django 5.1.7 on 2025-04-20 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("logsheet", "0027_glider_club_owned"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="maintenancedeadline",
            options={},
        ),
        migrations.RemoveField(
            model_name="maintenancedeadline",
            name="item",
        ),
        migrations.RemoveField(
            model_name="maintenancedeadline",
            name="notes",
        ),
        migrations.AddField(
            model_name="maintenancedeadline",
            name="description",
            field=models.CharField(
                choices=[
                    ("annual", "Annual Inspection"),
                    ("condition", "Condition Inspection"),
                    ("parachute", "Parachute Repack"),
                    ("transponder", "Transponder Inspection"),
                    ("letter", "Program Letter"),
                ],
                default="annual",
                help_text="Select type of maintenance deadline.",
                max_length=32,
            ),
            preserve_default=False,
        ),
    ]
