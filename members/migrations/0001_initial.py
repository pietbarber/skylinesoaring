# Generated by Django 5.1.7 on 2025-03-23 22:22

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
import tinymce.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="Member",
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
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        error_messages={
                            "unique": "A user with that username already exists."
                        },
                        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                        max_length=150,
                        unique=True,
                        validators=[
                            django.contrib.auth.validators.UnicodeUsernameValidator()
                        ],
                        verbose_name="username",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="first name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="last name"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True, max_length=254, verbose_name="email address"
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                ("SSA_member_number", models.CharField(max_length=20, unique=True)),
                ("phone", models.CharField(blank=True, max_length=20, null=True)),
                ("address", models.TextField(blank=True, null=True)),
                ("city", models.CharField(blank=True, max_length=50, null=True)),
                ("state", models.CharField(blank=True, max_length=20, null=True)),
                ("zip_code", models.CharField(blank=True, max_length=10, null=True)),
                (
                    "glider_rating",
                    models.CharField(
                        choices=[
                            ("student", "Student"),
                            ("transition", "Transition"),
                            ("private", "Private"),
                            ("commercial", "Commercial"),
                        ],
                        default="student",
                        max_length=10,
                    ),
                ),
                ("is_instructor", models.BooleanField(default=False)),
                ("is_duty_officer", models.BooleanField(default=False)),
                ("is_assistant_duty_officer", models.BooleanField(default=False)),
                ("secretary", models.BooleanField(default=False)),
                ("treasurer", models.BooleanField(default=False)),
                ("webmaster", models.BooleanField(default=False)),
                (
                    "glider_owned",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "second_glider_owned",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("joined_club", models.DateField(blank=True, null=True)),
                ("emergency_contact", models.TextField(blank=True, null=True)),
                ("public_notes", tinymce.models.HTMLField(blank=True, null=True)),
                ("private_notes", tinymce.models.HTMLField(blank=True, null=True)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "last_updated_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "abstract": False,
            },
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
