from django.db import models
from django.db.models import Sum


class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    external_id = models.CharField(max_length=60, unique=True)
    status = models.SmallIntegerField(default=1) #"Activo" (1) o "Inactivo" (2)
    score = models.DecimalField(max_digits=12, decimal_places=2)
    preapproved_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.external_id and not self.id:
            # Generar un nuevo external_id solo si no se proporciona
            last_customer = Customer.objects.order_by('-id').first()
            last_number = int(last_customer.external_id.split('_')[1]) if last_customer else 0
            self.external_id = f'external_{last_number + 1:02}'

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.external_id} - {self.status}'

    @property
    def total_debt(self):
        total_debt = self.loans.filter(status=2).aggregate(Sum('outstanding'))['outstanding__sum'] or 0
        return total_debt
    @property
    def available_amount(self):
        # total_debt = self.loans()
        # loans_outstanding = Loan.objects.filter(customer_id=customer, status__in=[2]).values_list('outstanding',
        #                                                                                           flat=True)
        # total_debt = sum(loans_outstanding)
        # loans_outstanding = Loan.objects.filter(customer_id=customer, status__in=[2]).values_list('outstanding',
        # total_debt = loans_outstanding
        available_amount = self.score - self.total_debt
        return available_amount

