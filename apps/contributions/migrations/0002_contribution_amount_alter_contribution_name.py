# Generated by Django 5.1.1 on 2024-11-29 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("contributions", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="contribution",
            name="amount",
            field=models.DecimalField(
                decimal_places=2, default=0, max_digits=5, verbose_name="Amount"
            ),
        ),
        migrations.AlterField(
            model_name="contribution",
            name="name",
            field=models.CharField(max_length=255, verbose_name="Name"),
        ),
    ]