import factory.django
from django_factory_boy.auth import UserFactory
from factory import LazyAttribute
from faker import Faker

from credit_card.models.credit_card import CreditCard

faker = Faker()


class CreditCardFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CreditCard

    user = factory.SubFactory(UserFactory)
    name = LazyAttribute(lambda _: faker.word())
    last_four_digits = LazyAttribute(lambda _: faker.random_number(digits=4))
    kind = LazyAttribute(
        lambda _: faker.random_int(min=CreditCard.Kind.CREDIT, max=CreditCard.Kind.CREDIT_DEBIT)
    )
