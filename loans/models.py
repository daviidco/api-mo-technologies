import locale

from django.db import models
from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from customers.models import Customer
from error_handler import CustomAPIException
from utils import get_total_outstanding


class Loan(models.Model):
    """
    STATUS:
    1: "pending" (pendiente) - el estado predeterminado cuando se crea el préstamo.
    2: "active" (activo) - una vez que se activa mediante un servicio, se debe actualizar la
    fecha de "taken_at".
    3: "rejected" (rechazado) - el préstamo puede ser rechazado solo si está en el estado 1
    ("pending").
    4: "paid" (pagado) - una vez que el préstamo ha sido completamente pagado y el valor
    de "outstanding" sea 0, se debe cambiar el estado a "paid".
    """

    STATUS_PENDING = 1
    STATUS_ACTIVE = 2
    STATUS_REJECTED = 3
    STATUS_PAID = 4

    STATUS_CHOICES = [
        (STATUS_PENDING, "pending"),
        (STATUS_ACTIVE, "active"),
        (STATUS_REJECTED, "rejected"),
        (STATUS_PAID, "paid"),
    ]

    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    external_id = models.CharField(max_length=60, unique=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=STATUS_PENDING)
    contract_version = models.CharField(max_length=30)
    maximum_payment_date = models.DateTimeField()
    taken_at = models.DateTimeField(null=True)
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="loans"
    )
    outstanding = models.DecimalField(max_digits=12, decimal_places=2)

    @property
    def customer_external_id(self):
        return self.customer.external_id

    def calculate_outstanding(self):
        # Sumar el monto total de los préstamos
        if not self.pk:
            return self.amount

        loan_amount_sum = self.amount

        # Sumar el monto total de los pagos relacionados al préstamo
        payment_amount_sum = (
            self.paymentdetail_set.filter(payment__status=1).aggregate(Sum("amount"))[
                "amount__sum"
            ]
            or 0
        )

        # Calcular el monto pendiente restando los pagos del préstamo
        outstanding = loan_amount_sum - payment_amount_sum
        return outstanding

    def save(self, *args, update_outstanding=True, **kwargs):
        # Actualizar el valor de 'outstanding' antes de guardar el objeto
        self.outstanding = self.calculate_outstanding()

        # Validar que tenga cupo
        total_outstanding = get_total_outstanding(self.customer)
        max_amount_loan = self.customer.score - total_outstanding
        if self.amount > max_amount_loan:
            max_amount_loan_formater = "{:,.2f}".format(abs(max_amount_loan))
            raise CustomAPIException(
                detail=f"El monto del prestamo excede el cupo. ${max_amount_loan_formater}"
            )

        if not self.external_id and not self.id:
            # Generar un nuevo external_id solo si no se proporciona
            last_loan = self.customer.loans.count()
            last_number = last_loan + 1
            customer_number = self.customer.external_id.split("_")[1]
            self.external_id = f"external_{customer_number}_{last_number:02}"

        super().save(*args, **kwargs)


@receiver(post_save, sender=Loan)
def update_taken_at(sender, instance, **kwargs):
    # Evitar la recursión para el caso específico de 'taken_at'
    if "update_taken_at" in kwargs:
        return

    # Desconectar temporalmente la señal para evitar el bucle de recursión
    post_save.disconnect(update_taken_at, sender=Loan)

    # Actualizar 'taken_at' cuando el estado sea 3 ("activo")
    if instance.status == 2:
        instance.taken_at = timezone.now()
        instance.outstanding = instance.amount
        instance.save()  # Pasar un argumento personalizado para evitar la recursión

    # Volver a conectar la señal después de realizar la actualización
    post_save.connect(update_taken_at, sender=Loan)
