from django.db import models


class ExchangeRate(models.Model):
    rate_type = models.CharField(max_length=50)  # e.g., 'blue', 'oficial', etc.
    origin_currency = models.CharField(max_length=10)  # e.g., 'USD'
    exchange_currency = models.CharField(max_length=10)  # e.g., 'ARS'
    buy_rate = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    sell_rate = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.rate_type} {self.origin_currency} to {self.exchange_currency}: Buy at {self.buy_rate}, Sell at {self.sell_rate} on {self.timestamp}"
