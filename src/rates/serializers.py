from rest_framework import serializers

from .models import ExchangeRate


class ExchangeRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeRate
        fields = ['id', 'rate_type', 'origin_currency', 'exchange_currency', 'buy_rate', 'sell_rate', 'timestamp']
