# Generated by Django 5.0b1 on 2023-11-29 21:30

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("credit_card", "0001_expense_category"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="CreditCard",
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
                    "name",
                    models.CharField(
                        help_text="The name printed in the credit card", max_length=128
                    ),
                ),
                (
                    "last_four_digits",
                    models.IntegerField(
                        help_text="The last four digits of the credit card number",
                    ),
                ),
                (
                    "kind",
                    models.IntegerField(
                        choices=[(1, "Credit"), (2, "Debit"), (3, "Credit and Debit")],
                        default=1,
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="credit_card",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
