from rest_framework import serializers
from .models import Customer


class CustomerGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        exclude = ['id', 'created_at', 'updated_at']


class CustomerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['score', 'preapproved_at', 'status', 'external_id']
        read_only_fields = ['status', 'external_id']


class CustomerBalanceSerializer(serializers.Serializer):
    external_id = serializers.CharField()
    score = serializers.FloatField()
    available_amount = serializers.FloatField()
    total_debt = serializers.FloatField()

