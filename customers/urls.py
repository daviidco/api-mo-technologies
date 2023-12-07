from django.urls import path, include
from rest_framework import routers

from .views import CustomerRetrieveView, CustomerListView, CustomerBalanceView

urlpatterns = [
    path('customers/', CustomerListView.as_view(), name='customer-list'),
    path('customers/<int:pk>/', CustomerRetrieveView.as_view(), name='customer-retrieve'),
    path('customers/<int:pk>/balance/', CustomerBalanceView.as_view(), name='customer-balance'),
]