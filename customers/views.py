from django.http import Http404
from rest_framework import generics, status
from rest_framework.views import APIView

from error_handler import CustomAPIException
from loans.models import Loan
from .models import Customer
from .serializers import CustomerGetSerializer, CustomerBalanceSerializer, CustomerCreateSerializer
from rest_framework.response import Response


class CustomerListView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CustomerGetSerializer
        elif self.request.method == 'POST':
            return CustomerCreateSerializer
        return CustomerGetSerializer  # Puedes cambiar esto según tus necesidades

    def create(self, request, *args, **kwargs):
        """
        Endpoint to list customers
        """
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        response_data = {
            'message': 'Customer created successfully',
            'data': serializer.data
        }
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)


class CustomerRetrieveView(generics.RetrieveAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerGetSerializer


class CustomerBalanceView(APIView):
    serializer_class = CustomerBalanceSerializer

    def get(self, request, *args, **kwargs):
        """
        Endpoint to get customer's balance
        """
        try:
            customer = Customer.objects.get(pk=kwargs['pk'])
        except Customer.DoesNotExist:
            raise CustomAPIException(detail='"Customer not found"')

        serializer = CustomerBalanceSerializer({
            'external_id': customer.external_id,
            'score': float(customer.score),
            'available_amount': float(customer.available_amount),
            'total_debt': float(customer.total_debt),
        })

        return Response(serializer.data)


