# Generated by Django 5.1.1 on 2024-11-29 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("info", "0005_activities_special_event"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="activities",
            options={"ordering": ("day",)},
        ),
        migrations.AlterField(
            model_name="activities",
            name="special_event",
            field=models.TextField(
                blank=True, null=True, verbose_name="Dodatkowe wydarzenia"
            ),
        ),
    ]