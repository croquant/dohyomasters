# Generated by Django 5.0.7 on 2024-07-17 14:20

import django_countries.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("rikishi", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="shusshin",
            options={
                "ordering": ["country", "prefecture"],
                "verbose_name_plural": "Shusshin",
            },
        ),
        migrations.RemoveField(
            model_name="shusshin",
            name="international",
        ),
        migrations.RemoveField(
            model_name="shusshin",
            name="name",
        ),
        migrations.AddField(
            model_name="shusshin",
            name="country",
            field=django_countries.fields.CountryField(
                default="JP", max_length=2
            ),
        ),
        migrations.AddField(
            model_name="shusshin",
            name="prefecture",
            field=models.CharField(
                blank=True, default=None, max_length=32, null=True
            ),
        ),
    ]
