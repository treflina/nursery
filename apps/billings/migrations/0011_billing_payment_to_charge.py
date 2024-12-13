# Generated by Django 5.1.1 on 2024-11-11 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("billings", "0010_alter_billing_child"),
    ]

    operations = [
        migrations.AddField(
            model_name="billing",
            name="payment_to_charge",
            field=models.DecimalField(
                decimal_places=2,
                default=0,
                max_digits=6,
                verbose_name="Payment to charge",
            ),
        ),
    ]
