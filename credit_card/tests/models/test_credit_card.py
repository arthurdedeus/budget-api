from django.test import TestCase

from credit_card.factories.credit_card import CreditCardFactory
from credit_card.models import CreditCard


class CreditCardModelTestCase(TestCase):
    def test_credit_card_model(self):
        CreditCardFactory()
        self.assertEqual(CreditCard.objects.count(), 1)
