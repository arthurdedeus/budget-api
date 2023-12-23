from django.db import models


class ExpenseCategory(models.Model):
    display_name = models.CharField(
        max_length=128,
        help_text="Display name of the category",
    )
    raw_name = models.CharField(
        help_text="Original name of the caterogy, obtained from csv statement. Used to match a new"
        "Expense to a customized ExpenseCategory.",
    )

    class Meta:
        verbose_name_plural = "Expense categories"
