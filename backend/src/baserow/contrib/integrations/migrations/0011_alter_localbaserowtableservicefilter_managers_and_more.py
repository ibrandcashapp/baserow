# Generated by Django 5.0.9 on 2025-02-07 17:23

from django.db import migrations

import baserow.contrib.integrations.local_baserow.models


class Migration(migrations.Migration):
    dependencies = [
        ("integrations", "0010_localbaserowaggregaterows"),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="localbaserowtableservicefilter",
            managers=[
                (
                    "objects",
                    baserow.contrib.integrations.local_baserow.models.LocalBaserowTableServiceRefinementManager(),
                ),
            ],
        ),
        migrations.AlterModelManagers(
            name="localbaserowtableservicesort",
            managers=[
                (
                    "objects",
                    baserow.contrib.integrations.local_baserow.models.LocalBaserowTableServiceRefinementManager(),
                ),
            ],
        ),
    ]
