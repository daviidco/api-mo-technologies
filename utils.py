from django.db.models import Sum

from customers.models import Customer


def get_total_outstanding(customer: Customer):
    return (
        customer.loans.filter(status=2).aggregate(Sum("outstanding"))[
            "outstanding__sum"
        ]
        or 0
    )
