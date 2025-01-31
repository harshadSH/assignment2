# Generated by Django 5.1.3 on 2025-01-22 05:34

import ckeditor.fields
import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0004_delete_blog"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Blog",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("title", models.CharField(max_length=200)),
                (
                    "image",
                    models.ImageField(blank=True, null=True, upload_to="blog_images/"),
                ),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("Mental Health", "Mental Health"),
                            ("Heart Disease", "Heart Disease"),
                            ("Covid19", "Covid19"),
                            ("Immunization", "Immunization"),
                        ],
                        max_length=50,
                    ),
                ),
                ("summary", models.TextField(max_length=500)),
                ("content", ckeditor.fields.RichTextField()),
                ("is_draft", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
