import json
from decimal import Decimal

from django.http import HttpResponseForbidden, HttpResponse
from django.shortcuts import get_object_or_404
from django.core.signing import Signer
from rest_framework import generics, status
from rest_framework.response import Response
from oscar.core.loading import get_model
from oscarapicheckout import utils

from apps.checkout.creditcards import serializers
from apps.checkout.creditcards.mixins import PaymentMixin
from apps.checkout.creditcards.tinkoff import Tinkoff
from .methods import CreditCard
import uuid

Order = get_model('order', 'Order')


#
# class AuthorizeCardView(generics.GenericAPIView):
#     def post(self, request):
#         # Mark the payment method as complete or denied
#         amount = Decimal(request.data['amount'])
#         order_number = request.data['reference_number']
#         order = get_object_or_404(Order, number=order_number)
#
#         # Get the method key
#         method_key = Signer().unsign(request.data['transaction_id'])
#
#         # Decline the payment
#         if request.data.get('deny'):
#             utils.mark_payment_method_declined(order, request, method_key, request.data['amount'])
#             return Response({
#                 'status': 'Declined',
#             })
#
#         # Record the funds allocation
#         new_state = CreditCard().record_successful_authorization(order, amount, uuid.uuid1())
#         utils.update_payment_method_state(order, request, method_key, new_state)
#         return Response({
#             'status': 'Success',
#         })



class NotificationView(generics.GenericAPIView):
    serializer_class = serializers.AuthorizeSerializer

    def post(self, request):
        print('-----------------------------------------------------------------')
        #   received_json_data = json.loads(request.body)
        object = request.data

        token = object['Token']
        object['Success'] = str(object['Success']).lower()
        print(token)
        object.pop("Token")
        print(object)

        tinkoff = Tinkoff()
        hash_string = tinkoff.create_hash(object)
        print(hash_string)
        if hash_string != token:
            print('Validate: FALSE')
            return HttpResponseForbidden()

        print('Validate: TRUE')

        order = get_object_or_404(Order, number=object['OrderId'])
        if object['Status'] == 'CONFIRMED':
            new_state = CreditCard().record_successful_authorization(order, order.total_incl_tax, uuid.uuid1())
            utils.update_payment_method_state(order, request, order.number, new_state)

        return HttpResponse('OK', status=status.HTTP_200_OK)
