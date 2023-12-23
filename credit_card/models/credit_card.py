from django.contrib.auth import get_user_model
from django.db import models


class CreditCard(models.Model):
    class Kind(models.IntegerChoices):
        CREDIT = 1, "Credit"
        DEBIT = 2, "Debit"
        CREDIT_DEBIT = 3, "Credit and Debit"

    user = models.ForeignKey(
        get_user_model(),
        related_name="credit_card",
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        max_length=128,
        help_text="The name printed in the credit card",
    )
    last_four_digits = models.IntegerField(
        help_text="The last four digits of the credit card number",
    )
    kind = models.IntegerField(
        choices=Kind.choices,
        default=Kind.CREDIT,
    )
