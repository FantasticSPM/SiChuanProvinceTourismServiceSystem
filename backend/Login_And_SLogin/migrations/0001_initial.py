# Generated by Django 4.2 on 2023-04-28 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="UserTable",
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
                ("user_name", models.CharField(max_length=20, unique=True)),
                ("user_password", models.CharField(max_length=64)),
                ("user_age", models.IntegerField(blank=True)),
                ("user_xs", models.CharField(blank=True, max_length=2)),
            ],
        ),
    ]
