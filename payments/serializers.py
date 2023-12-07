from rest_framework import serializers

from loans.models import Loan
from payments.models import Payment, PaymentDetail
from .models import Payment
from .validators import validate_payment_amount


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = PaymentDetail
        fields = ['external_id', 'customer_external_id', 'loan_external_id','payment_date', 'status', 'total_amount', 'payment_amount']



class PaymentDetailSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=20, decimal_places=10)
    loan_id = serializers.IntegerField(required=True)

    def create(self, validated_data):
        # Implementa la lógica de creación de pagos aquí
        return PaymentDetail.objects.create(**validated_data)



class PaymentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['status']
