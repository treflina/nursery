# Generated by Django 5.1.1 on 2024-10-31 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0005_rename_date_additionaldayoff_day"),
    ]

    operations = [
        migrations.CreateModel(
            name="MonthlyPayment",
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
                (
                    "price",
                    models.DecimalField(
                        decimal_places=2, default=0, max_digits=6, verbose_name="Price"
                    ),
                ),
            ],
        ),
    ]