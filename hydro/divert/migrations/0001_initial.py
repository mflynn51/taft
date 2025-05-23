# Generated by Django 5.1.4 on 2024-12-23 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="GeoPoint",
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
                ("latitude", models.FloatField()),
                ("longitude", models.FloatField()),
                ("pod", models.CharField(max_length=100)),
                ("podType", models.CharField(max_length=12)),
                ("podRate", models.IntegerField()),
                ("units", models.CharField(max_length=12)),
                ("podStorage", models.IntegerField()),
                ("owner", models.CharField(max_length=100)),
                ("faceValueAF", models.IntegerField()),
                ("maxDiversionFlow", models.IntegerField()),
                ("unitsFlow", models.CharField(max_length=12)),
                ("status", models.CharField(max_length=12)),
            ],
        ),
    ]
