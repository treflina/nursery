# Generated by Django 5.1.1 on 2024-10-30 15:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0004_additionaldayoff"),
    ]

    operations = [
        migrations.RenameField(
            model_name="additionaldayoff",
            old_name="date",
            new_name="day",
        ),
    ]