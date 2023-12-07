from django.urls import path, include
from rest_framework import routers

from .views import CustomerRetrieveView, CustomerListView, CustomerBalanceView

# router = routers.DefaultRouter()
# router.register(r'api/customers', CustomerListCreateView)
# router.register(r'api/customers/<int:pk>/', CustomerDetailView)
# router.register(r'api/customers/all/', AllCustomersListView)
# router.register(r'api/customers/delete/<int:pk>/', CustomerDeleteView)
# router.register(r'api/customers/update/<int:pk>/', CustomerUpdateView)


# urlpatterns = [
#     path('', include(router.urls))
# ]

urlpatterns = [
    # path('customers/', CustomerListCreateView.as_view(), name='movie-list-create'),
    path('customers/', CustomerListView.as_view(), name='customer-list'),
    path('customers/<int:pk>/', CustomerRetrieveView.as_view(), name='customer-retrieve'),
    path('customers/<int:pk>/balance/', CustomerBalanceView.as_view(), name='customer-balance'),
]