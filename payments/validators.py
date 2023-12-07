from rest_framework import serializers


def validate_payment_amount(value):
    if value < 0:
        raise serializers.ValidationError("El monto del pago debe ser mayor que cero.")
