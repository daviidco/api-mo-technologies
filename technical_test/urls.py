"""
URL configuration for technical_test project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
# from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# from rest_framework_api_key.permissions import HasAPIKey





schema_view = get_schema_view(
   openapi.Info(
      title="MO Technologies API",
      default_version='v1',
      description="En MO Technologies, nos especializamos en impulsar las soluciones de crédito digital más ambiciosas en LATAM. Nuestro objetivo es habilitar y empoderar a las empresas para que puedan lanzar productos de crédito innovadores y adaptados a las necesidades del mercado para que siempre estén a la vanguardia.",
      terms_of_service="https://www.linkedin.com/company/motechnologies/",
      contact=openapi.Contact(email="daviidco@hotmail.com"),
      license=openapi.License(name="BSD License"),
   ),
    public=True,
    # permission_classes=(permissions.AllowAny),
    # authentication_classes=(HasAPIKey,),

)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('customers/', include('customers.urls')),
    path('loans/', include('loans.urls')),
    path('payments/', include('payments.urls')),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


