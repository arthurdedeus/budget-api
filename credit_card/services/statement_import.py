import logging
from datetime import datetime

import pandas as pd

from credit_card.models import CreditCard, Expense, ExpenseCategory
from credit_card.services.constants import C6BankStatementColumns

logger = logging.getLogger(__name__)


class StatementImportService:
    columns = C6BankStatementColumns

    def __init__(self, user, filename):
        self.file = pd.read_csv(filename, sep=";", header=0, usecols=self.columns.list())
        self.user = user

    def process_file(self):
        file = self._group_by_credit_card(self.file)
        for index, row in file.iterrows():
            card = self._get_or_create_credit_card(row)
            self._create_expenses(card, row)

    def _get_or_create_credit_card(self, row):
        last_four_digits, name = row.name
        card, created = CreditCard.objects.get_or_create(
            last_four_digits=last_four_digits, name=name, user=self.user
        )
        if created:
            logger.info("Created CreditCard", extra={"credit_card_id": card.id})
        return card

    def _create_expenses(self, card, row):
        objects_to_create = []
        for date, category, description, installments, amount in zip(
            row[self.columns.DATE],
            row[self.columns.CATEGORY],
            row[self.columns.DESCRIPTION],
            row[self.columns.INSTALLMENT],
            row[self.columns.AMOUNT],
        ):
            installment, total_installments = self._parse_installments(installments)
            expense = Expense(
                card=card,
                category=self._get_or_create_category(category),
                date=datetime.strptime(date, "%d/%m/%Y"),
                description=description.strip(),
                amount=amount,
                installment=installment,
                total_installments=total_installments,
            )
            objects_to_create.append(expense)
        return Expense.objects.bulk_create(objects_to_create)

    @staticmethod
    def _get_or_create_category(category):
        expense_category, created = ExpenseCategory.objects.get_or_create(
            raw_name=category, defaults={"display_name": category}
        )
        if created:
            logger.info(
                "Created ExpenseCategory", extra={"expense_category_id": expense_category.id}
            )
        return expense_category

    @staticmethod
    def _parse_installments(installments):
        if installments == "Única":
            return 1, 1
        try:
            installment, total_installments = installments.split("/")
            return int(installment), int(total_installments)
        except IndexError:
            logger.info(
                "Installment value with no slash",
                extra={"installments": installments},
                exc_info=True,
            )
            return 1, 1
        except ValueError:
            logger.info(
                "Bad installment or total installments value",
                extra={"installments": installments},
                exc_info=True,
            )
            return 1, 1
        except AttributeError:
            logger.info("No installment value", extra={"installments": installments}, exc_info=True)
            return 1, 1

    def _group_by_credit_card(self, file):
        return file.groupby([self.columns.LAST_4_DIGITS, self.columns.NAME]).agg(list)
