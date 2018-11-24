import hashlib
import json

import requests
from django.conf import settings
from django.core.signing import Signer
from rest_framework.reverse import reverse
from oscarapicheckout.methods import PaymentMethod, PaymentMethodSerializer
from oscarapicheckout.states import FormPostRequired, Complete

from .tinkoff import Tinkoff


class CreditCard(PaymentMethod):
    """
    This is an example of how to implement a payment method that required some off-site
    interaction, like Cybersource Secure Acceptance, for example. It returns a pending
    status initially that requires the client app to make a form post, which in-turn
    redirects back to us. This is a common pattern in PCI SAQ A-EP ecommerce sites.
    """
    name = 'Tinkoff'
    code = 'tinkoff'
    serializer_class = PaymentMethodSerializer

    tinkoff = Tinkoff()

    # Payment Step 1
    def _record_payment(self, request, order, method_key, amount, reference, **kwargs):
        fields = [

        ]
        tinkoff = self.require_authorization_post(order, '', amount)
        result = FormPostRequired(
            amount=amount,
            name='get-token',
            url=tinkoff['PaymentURL'],
            fields=fields)
        return result



    # Payment Step 2
    def require_authorization_post(self, order, method_key, amount):

        return self.tinkoff.init_order(order, amount)

    # Payment Step 3
    def record_successful_authorization(self, order, amount, reference):
        source = self.get_source(order, reference)

        source.allocate(amount, reference)
        event = self.make_authorize_event(order, amount, reference)
        for line in order.lines.all():
            self.make_event_quantity(event, line, line.quantity)

        return Complete(amount)


