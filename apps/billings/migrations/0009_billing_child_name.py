# Generated by Django 5.1.1 on 2024-11-11 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("billings", "0008_billing_confirmed_billing_sent"),
    ]

    operations = [
        migrations.AddField(
            model_name="billing",
            name="child_name",
            field=models.CharField(
                default="", max_length=255, verbose_name="Child's name"
            ),
        ),
    ]