# Generated by Django 5.1.1 on 2024-10-28 09:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("kids", "0002_initial"),
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="child",
            name="parent",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="users.parent",
            ),
        ),
    ]
