# Generated by Django 5.1.1 on 2024-10-31 19:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0008_alter_monthlypayment_price"),
        ("kids", "0004_child_gov_subsidy_child_other_subsidy"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="child",
            name="gov_subsidy",
        ),
        migrations.AlterField(
            model_name="child",
            name="local_subsidy",
            field=models.BooleanField(default=True, verbose_name="Subsidy"),
        ),
        migrations.AlterField(
            model_name="child",
            name="other_subsidy",
            field=models.ManyToManyField(
                to="core.othersubsidy", verbose_name="Other subsidies"
            ),
        ),
        migrations.AddField(
            model_name="child",
            name="gov_subsidy",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="core.governmentsubsidy",
                verbose_name="Government subsidy",
            ),
        ),
    ]