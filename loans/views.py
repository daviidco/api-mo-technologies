from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action

from .models import Loan, Customer
from .serializers import LoanSerializer, LoanUpdateSerializer

from rest_framework import generics, status, viewsets
from rest_framework.response import Response


class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

    def list(self, request, pk=None):
        """
        Endpoint to list customer's loans.
        """
        # Obtener todos los préstamos para un cliente específico
        loans = Loan.objects.filter(customer_id=pk)
        serializer = self.get_serializer(loans, many=True)
        return Response(serializer.data)

    def create(self, request, pk=None):
        """
        Endpoint to create a loan.
        """
        # Crear un nuevo préstamo para un cliente específico
        customer = Customer.objects.get(id=pk)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(customer=customer)
        # self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        response_data = {
            "message": "Préstamo creado exitosamente",
            "data": serializer.data,
        }
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=["PATCH"])
    @swagger_auto_schema(
        request_body=LoanUpdateSerializer,  # Usar el serializer de actualización
        responses={
            status.HTTP_200_OK: LoanSerializer()
        },  # Puedes ajustar según tus necesidades
    )
    def partial_update(self, request, pk=None):
        """
        Endpoint to patch loan's status
        """
        # Obtener la instancia del Loan que se actualizará
        loan = self.get_object()

        # Crear una instancia de LoanUpdateSerializer con la instancia existente y los datos del request
        serializer = LoanUpdateSerializer(loan, data=request.data, partial=True)

        # Validar y guardar la actualización
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Retornar el objeto Loan actualizado utilizando el serializer original
        updated_loan = Loan.objects.get(pk=pk)  # Obtener la instancia actualizada
        updated_serializer = LoanSerializer(
            updated_loan
        )  # Utilizar el serializer original
        response_data = {
            "message": "Actualización parcial exitosa",
            "data": updated_serializer.data,
        }
        return Response(response_data, status=status.HTTP_200_OK)
