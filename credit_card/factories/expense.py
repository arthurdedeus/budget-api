import factory
from factory import LazyAttribute
from faker import Faker

from credit_card.factories.credit_card import CreditCardFactory
from credit_card.factories.expense_category import ExpenseCategoryFactory
from credit_card.models.expense import Expense

faker = Faker()


class ExpenseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Expense

    card = factory.SubFactory(CreditCardFactory)
    category = factory.SubFactory(ExpenseCategoryFactory)
    date = LazyAttribute(lambda _: faker.date())
    description = LazyAttribute(lambda _: faker.word())
    amount = LazyAttribute(lambda _: faker.random_int(min=1, max=999999))
    installment = LazyAttribute(lambda _: faker.random_int(min=1, max=12))
    total_installments = LazyAttribute(lambda obj: faker.random_int(min=obj.installment, max=12))
