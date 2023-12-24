from django.db import models


class Expense(models.Model):
    card = models.ForeignKey(
        "credit_card.CreditCard",
        related_name="expenses",
        on_delete=models.CASCADE,
    )
    category = models.ForeignKey(
        "credit_card.ExpenseCategory",
        related_name="expenses",
        on_delete=models.SET_NULL,
        null=True,
    )
    date = models.DateField()
    description = models.CharField(max_length=128)
    amount = models.IntegerField()
    total_installments = models.IntegerField(default=1)
    installment = models.IntegerField(default=1)
