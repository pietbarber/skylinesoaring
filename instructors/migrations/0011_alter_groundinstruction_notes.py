# Generated by Django 5.1.7 on 2025-04-13 15:48

import tinymce.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("instructors", "0010_remove_groundinstruction_lessons_groundlessonscore"),
    ]

    operations = [
        migrations.AlterField(
            model_name="groundinstruction",
            name="notes",
            field=tinymce.models.HTMLField(blank=True, null=True),
        ),
    ]
