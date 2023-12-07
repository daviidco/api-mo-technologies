from django.urls import path

from loans.views import LoanViewSet

urlpatterns = [
    path(
        "customers/<int:pk>/",
        LoanViewSet.as_view({"get": "list", "post": "create"}),
        name="loan-create-get",
    ),
    path(
        "<int:pk>/", LoanViewSet.as_view({"patch": "partial_update"}), name="loan-patch"
    ),
]
