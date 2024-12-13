# Generated by Django 5.1.1 on 2024-11-11 18:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0008_alter_monthlypayment_price"),
        ("kids", "0008_child_payment_month"),
    ]

    operations = [
        migrations.AlterField(
            model_name="child",
            name="payment_month",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="core.monthlypayment",
                verbose_name="Monthly payment",
            ),
        ),
    ]
