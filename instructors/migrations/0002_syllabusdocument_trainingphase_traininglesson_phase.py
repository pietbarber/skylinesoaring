# Generated by Django 5.1.7 on 2025-04-11 22:59

import django.db.models.deletion
import tinymce.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("instructors", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="SyllabusDocument",
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
                ("slug", models.SlugField(unique=True)),
                ("title", models.CharField(max_length=200)),
                ("content", tinymce.models.HTMLField()),
            ],
        ),
        migrations.CreateModel(
            name="TrainingPhase",
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
                ("number", models.PositiveSmallIntegerField()),
                ("name", models.CharField(max_length=100)),
            ],
            options={
                "ordering": ["number"],
            },
        ),
        migrations.AddField(
            model_name="traininglesson",
            name="phase",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="lessons",
                to="instructors.trainingphase",
            ),
        ),
    ]
