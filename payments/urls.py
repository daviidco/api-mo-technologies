from django.urls import path

from payments.views import PaymentViewSet


urlpatterns = [
    path(
        "customers/<int:pk>/",
        PaymentViewSet.as_view({"get": "list", "post": "create"}),
        name="payment-create-get",
    ),
    path(
        "<int:pk>/",
        PaymentViewSet.as_view({"patch": "partial_update"}),
        name="loan-patch",
    ),
]
