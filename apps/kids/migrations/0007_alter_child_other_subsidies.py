# Generated by Django 5.1.1 on 2024-10-31 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0008_alter_monthlypayment_price"),
        ("kids", "0006_rename_other_subsidy_child_other_subsidies"),
    ]

    operations = [
        migrations.AlterField(
            model_name="child",
            name="other_subsidies",
            field=models.ManyToManyField(
                blank=True,
                null=True,
                to="core.othersubsidy",
                verbose_name="Other subsidies",
            ),
        ),
    ]