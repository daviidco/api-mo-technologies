from django.urls import path, include
from rest_framework import routers

from .views import CustomerRetrieveView, CustomerListView, CustomerBalanceView

urlpatterns = [
    path("", CustomerListView.as_view(), name="customer-list"),
    path("<int:pk>/", CustomerRetrieveView.as_view(), name="customer-retrieve"),
    path("<int:pk>/balance/", CustomerBalanceView.as_view(), name="customer-balance"),
]
