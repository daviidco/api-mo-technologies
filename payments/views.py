from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from customers.models import Customer
from error_handler import CustomAPIException
from loans.models import Loan
from .models import Payment, PaymentDetail
from .serializers import (
    PaymentSerializer,
    PaymentUpdateSerializer,
    PaymentDetailSerializer,
)


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = PaymentDetail.objects.all()
    serializer_class = PaymentSerializer

    def list(self, request, pk=None):
        """
        Endpoint to list payments by customer's id
        """
        # Obtener todos los préstamos para un cliente específico
        payments = Payment.objects.filter(customer_id=pk)
        serializer = self.get_serializer(payments, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["POST"])
    @swagger_auto_schema(
        request_body=PaymentDetailSerializer(
            many=True
        ),  # Usar el serializer de actualización
        responses={
            status.HTTP_201_CREATED: PaymentSerializer()
        },  # Puedes ajustar según tus necesidades
    )
    def validate_payment_amount_vs_lound_amount(self, payment, loan_instance):
        if loan_instance.status == Loan.STATUS_PAID:
            raise CustomAPIException(
                detail=f"El prestamo {loan_instance.id} ya está pagado"
            )
        if float(payment.get("amount")) > loan_instance.outstanding:
            raise CustomAPIException(
                detail=f"El monto a pagar supera la deuda del prestamo {loan_instance.id}"
            )

    def create(self, request, pk=None):
        """
        Endpoint to create payment
        """
        # Verificar si los datos son una lista
        is_list_data = isinstance(request.data, list)
        total_amount = sum(int(payment["amount"]) for payment in request.data)

        for payment in request.data:
            try:
                loan_instance = Loan.objects.get(id=payment.get("loan_id"))
            except Loan.DoesNotExist:
                raise CustomAPIException(detail='"Loan not found"')

            self.validate_payment_amount_vs_lound_amount(payment, loan_instance)

            # Crear la instancia de Payment
            payment_instance = Payment.objects.create(
                total_amount=total_amount, customer=Customer.objects.get(id=pk)
            )

            # Utilizar el serializer correspondiente dependiendo de si es una lista o no
            serializer = PaymentDetailSerializer(data=payment)
            serializer.is_valid(raise_exception=True)

            serializer.save(payment=payment_instance)

        headers = self.get_success_headers(serializer.data)
        response_data = {
            "message": "Pago(s) creado(s) exitosamente",
            "data": serializer.data,
        }
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=["PATCH"])
    @swagger_auto_schema(
        request_body=PaymentUpdateSerializer,  # Usar el serializer de actualización
        responses={
            status.HTTP_200_OK: PaymentSerializer()
        },  # Puedes ajustar según tus necesidades
    )
    def partial_update(self, request, pk=None):
        """
        Endpoint to patch payment's status
        """
        # Obtener la instancia del Payment que se actualizará
        payment = Payment.objects.get(id=pk)

        # Crear una instancia de PaymentUpdateSerializer con la instancia existente y los datos del request
        serializer = PaymentUpdateSerializer(payment, data=request.data, partial=True)

        # Validar y guardar la actualización
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Retornar el objeto Payment actualizado utilizando el serializer original
        updated_payment = Payment.objects.get(pk=pk)  # Obtener la instancia actualizada
        updated_serializer = PaymentSerializer(
            updated_payment
        )  # Utilizar el serializer original
        response_data = {
            "message": "Actualización parcial exitosa",
            "data": updated_serializer.data,
        }
        return Response(response_data, status=status.HTTP_200_OK)
