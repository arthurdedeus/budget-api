from django.contrib import admin

from credit_card.models import CreditCard, ExpenseCategory


@admin.register(ExpenseCategory)
class ExpenseCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(CreditCard)
class CreditCardAdmin(admin.ModelAdmin):
    pass
