from django.test import TestCase

from credit_card.factories.expense import ExpenseFactory
from credit_card.models import Expense


class ExpenseModelTestCase(TestCase):
    def test_expense_model(self):
        ExpenseFactory()
        self.assertEqual(Expense.objects.count(), 1)
