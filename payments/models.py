
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from customers.models import Customer
from error_handler import CustomAPIException
from loans.models import Loan
from utils import get_total_outstanding


class Payment(models.Model):
    STATUS_COMPLETED = 1
    STATUS_REJECTED = 2

    STATUS_CHOICES = [
        (STATUS_COMPLETED, "completed"),
        (STATUS_REJECTED, "rejected"),
    ]


    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    external_id = models.CharField(max_length=60, unique=True)
    total_amount = models.DecimalField(max_digits=20, decimal_places=10)
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=STATUS_COMPLETED)
    paid_at = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='payments')

    def save(self, *args, **kwargs):
        # Validar si el cliente tiene préstamos activos
        if not self.customer.loans.filter(status=2).exists():
            raise CustomAPIException(detail='El cliente no tiene préstamos activos.')

        # Validar que el pago no exceda el monto de la deuda
        # total_outstanding = self.customer.loans.filter(status=2).aggregate(Sum('outstanding'))['outstanding__sum'] or 0
        total_outstanding = get_total_outstanding(self.customer)
        if self.total_amount > total_outstanding:
            raise CustomAPIException(detail='El monto del pago excede la deuda del cliente.')

        if not self.external_id and not self.id:
            # Generar un nuevo external_id solo si no se proporciona
            last_payment = self.customer.payments.count()
            last_number = last_payment + 1
            customer_number = self.customer.external_id.split('_')[1]
            self.external_id = f'external_{customer_number}_{last_number:02}'

        super().save(*args, **kwargs)



class PaymentDetail(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    amount = models.DecimalField(max_digits=20, decimal_places=10)
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)

    @property
    def external_id(self):
        return self.payment.customer.external_id

    @property
    def customer_external_id(self):
        return self.payment.customer.external_id

    @property
    def loan_external_id(self):
        return self.loan.external_id

    @property
    def payment_date(self):
        return self.payment.paid_at

    @property
    def status(self):
        return self.payment.status

    @property
    def total_amount(self):
        return self.payment.total_amount

    @property
    def payment_amount(self):
        return self.amount

@receiver(post_save, sender=PaymentDetail)
def hadle_check_(sender, instance, **kwargs):
    # Actualizar el estado a "paid" si 'outstanding' llega a 0
    if instance.loan.outstanding == 0:
        instance.loan.status = Loan.STATUS_PAID
        instance.loan.save(update_outstanding=False)


# Extra
@receiver(post_save, sender=Payment)
def handle_rejected_payment(sender, instance, **kwargs):
    if instance.status == Payment.STATUS_REJECTED:
        # Obtener los detalles de préstamos asociados al pago rechazado
        loan_details = instance.loan_details.all()

        for detail in loan_details:
            # Actualizar el 'outstanding' del préstamo
            detail.loan.outstanding += detail.amount_paid
            detail.loan.status = Loan.STATUS_ACTIVE  # Opcional: cambiar el estado a "active"
            detail.loan.save()