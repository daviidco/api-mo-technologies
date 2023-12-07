from rest_framework import serializers
from .models import Loan


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = [
            "external_id",
            "amount",
            "outstanding",
            "status",
            "contract_version",
            "maximum_payment_date",
            "customer_external_id",
        ]
        read_only_fields = [
            "external_id",
            "outstanding",
            "status",
            "customer_external_id",
        ]


class LoanUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ["status"]

    def validate_status(self, value):
        # Obtener el estado actual del préstamo
        current_status = self.instance.status if self.instance else None

        # Obtener el valor anterior de 'outstanding'
        previous_outstanding = self.instance.outstanding if self.instance else 0

        # Validar los estados permitidos
        allowed_statuses = {
            1: "pending",
            2: "active",
            3: "rejected",
            4: "paid",
        }

        if value not in allowed_statuses:
            raise serializers.ValidationError("Estado no válido")

        # Validaciones específicas para cada estado
        if value == 2:  # active
            if current_status != 1:
                raise serializers.ValidationError(
                    "El estado debe ser 'pending' para activar el préstamo."
                )
            # Realizar otras validaciones si es necesario

        elif value == 3:  # rejected
            if current_status != 1:
                raise serializers.ValidationError(
                    "El estado debe ser 'pending' para rechazar el préstamo."
                )
            # Realizar otras validaciones si es necesario

        elif value == 4:  # paid
            if previous_outstanding != 0:
                raise serializers.ValidationError(
                    "El préstamo debe tener un valor 'outstanding' de 0 para cambiar a 'paid'."
                )
            # Realizar otras validaciones si es necesario

        return value
