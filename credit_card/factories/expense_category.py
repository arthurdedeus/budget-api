import factory
from factory import LazyAttribute
from faker import Faker

from credit_card.models.expense_category import ExpenseCategory

faker = Faker()


class ExpenseCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ExpenseCategory

    raw_name = LazyAttribute(lambda _: faker.word())
    display_name = LazyAttribute(lambda _: faker.word())
