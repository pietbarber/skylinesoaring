# Generated by Django 5.1.7 on 2025-04-12 00:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("instructors", "0004_instructionreport"),
    ]

    operations = [
        migrations.CreateModel(
            name="LessonScore",
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
                    "score",
                    models.CharField(
                        choices=[
                            ("1", "Introduced (Instructor flew)"),
                            ("2", "Practiced (with instructor help)"),
                            ("3", "Solo Standard"),
                            ("4", "Checkride Standard"),
                            ("!", "Needs Attention (!)"),
                        ],
                        max_length=2,
                    ),
                ),
                ("notes", models.TextField(blank=True)),
                (
                    "lesson",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="instructors.traininglesson",
                    ),
                ),
                (
                    "report",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="lesson_scores",
                        to="instructors.instructionreport",
                    ),
                ),
            ],
            options={
                "ordering": ["lesson__code"],
                "unique_together": {("report", "lesson")},
            },
        ),
    ]
