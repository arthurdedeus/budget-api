import pandas as pd
from django.test import TestCase
from django_factory_boy.auth import UserFactory

from credit_card.factories.credit_card import CreditCardFactory
from credit_card.factories.expense_category import ExpenseCategoryFactory
from credit_card.models import CreditCard, Expense, ExpenseCategory
from credit_card.services.constants import C6BankStatementColumns
from credit_card.services.statement_import import StatementImportService

GAMBLING = "Gambling"
FOO = "Foo"
RAW_FILE_PATH = "credit_card/tests/services/data/c6-statement.csv"
GROUPED_FILE_PATH = "credit_card/tests/services/data/grouped-by-card.json"


class ImportServiceTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.raw_file = pd.read_csv(RAW_FILE_PATH, sep=";")
        self.grouped_file = pd.read_json(GROUPED_FILE_PATH)
        self.svc = StatementImportService(self.user, filename=RAW_FILE_PATH)

    def test_import_service(self):
        self.assertEqual(CreditCard.objects.count(), 0)
        self.assertEqual(Expense.objects.count(), 0)
        self.assertEqual(ExpenseCategory.objects.count(), 0)

        self.svc.process_file()

        self.assertEqual(CreditCard.objects.count(), 2)
        self.assertEqual(Expense.objects.count(), 9)
        self.assertEqual(ExpenseCategory.objects.count(), 4)

    def test_get_or_create_credit_card_when_it_creates(self):
        row = pd.Series(name=(1234, FOO))
        self.assertEqual(CreditCard.objects.count(), 0)

        result = self.svc._get_or_create_credit_card(row)

        self.assertEqual(CreditCard.objects.count(), 1)
        self.assertEqual(result.last_four_digits, 1234)
        self.assertEqual(result.name, FOO)
        self.assertEqual(result.user, self.user)

    def test_get_or_create_credit_card_when_it_gets(self):
        row = pd.Series(name=(1234, FOO))
        CreditCardFactory(last_four_digits=1234, name=FOO, user=self.user)
        self.assertEqual(CreditCard.objects.count(), 1)

        result = self.svc._get_or_create_credit_card(row)

        self.assertEqual(CreditCard.objects.count(), 1)
        self.assertEqual(result.last_four_digits, 1234)
        self.assertEqual(result.name, FOO)
        self.assertEqual(result.user, self.user)

    def test_create_expenses(self):
        card = CreditCardFactory()
        row = self.grouped_file.iloc[0]

        results = self.svc._create_expenses(card, row)

        self.assertEqual(len(results), 3)
        self.assertEqual(Expense.objects.count(), 3)
        self.assertEqual(card.expenses.count(), 3)

    def test_get_or_create_category_when_it_creates(self):
        self.assertEqual(ExpenseCategory.objects.count(), 0)

        result = StatementImportService._get_or_create_category(GAMBLING)

        self.assertEqual(ExpenseCategory.objects.count(), 1)
        self.assertEqual(result.raw_name, GAMBLING)
        self.assertEqual(result.display_name, GAMBLING)

    def test_get_or_create_category_when_it_gets(self):
        ExpenseCategoryFactory(raw_name=GAMBLING, display_name="Bingo")
        self.assertEqual(ExpenseCategory.objects.count(), 1)

        result = StatementImportService._get_or_create_category(GAMBLING)

        self.assertEqual(ExpenseCategory.objects.count(), 1)
        self.assertEqual(result.raw_name, GAMBLING)
        self.assertEqual(result.display_name, "Bingo")

    def test_parse_installments(self):
        arguments = [
            ("valid installments", "1/6", 1, 6),
            ("single installment", "Única", 1, 1),
            ("random string", "foo", 1, 1),
            ("string with slash but invalid characters", "foo/bar", 1, 1),
            ("empty string", "", 1, 1),
            ("null", None, 1, 1),
        ]
        for msg, installments, expected_installment, expected_total_installments in arguments:
            with self.subTest(msg):
                (
                    result_installment,
                    result_total_installments,
                ) = StatementImportService._parse_installments(installments)
                self.assertEqual(result_installment, expected_installment)
                self.assertEqual(result_total_installments, expected_total_installments)

    def test_group_by_credit_card(self):
        result = StatementImportService._group_by_credit_card(self.raw_file)

        self.assertEqual(self.raw_file.shape, (9, 9))
        self.assertEqual(self.raw_file[C6BankStatementColumns.LAST_4_DIGITS].nunique(), 2)
        self.assertEqual(result.shape, (2, 7))
