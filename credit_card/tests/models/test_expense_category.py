from django.test import TestCase

from credit_card.factories.expense_category import ExpenseCategoryFactory
from credit_card.models import ExpenseCategory


class ExpenseCategoryModelTestCase(TestCase):
    def test_credit_card_model(self):
        ExpenseCategoryFactory()
        self.assertEqual(ExpenseCategory.objects.count(), 1)
