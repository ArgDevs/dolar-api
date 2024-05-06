from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ExchangeRateViewSet

router = DefaultRouter()
router.register(r'exchange_rates', ExchangeRateViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
