import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand

from rates.models import ExchangeRate
from rates.scraper import scrape_exchange_rates


class Command(BaseCommand):
    help = 'Scrapes exchange rates and stores them in the database if they have changed'

    def handle(self, *args, **options):
        self.stdout.write("Starting to scrape exchange rates...")

        try:
            url = 'https://dolarhoy.com/'
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            rates = scrape_exchange_rates(soup)

            for rate_type, rate_info in rates.items():
                # Convert 'N/A' to -1
                buy_rate = rate_info['Compra'] if rate_info['Compra'] != 'N/A' else -1
                sell_rate = rate_info['Venta'] if rate_info['Venta'] != 'N/A' else -1

                # Retrieve the most recent rate from the database for this type
                latest_rate = ExchangeRate.objects.filter(rate_type=rate_type).order_by('-timestamp').first()

                # Check if the most recent record has different rates
                if (not latest_rate or
                    float(latest_rate.buy_rate) != float(buy_rate) or
                    float(latest_rate.sell_rate) != float(sell_rate)):
                    ExchangeRate.objects.create(
                        rate_type=rate_type,
                        origin_currency='USD',
                        exchange_currency='ARS',
                        buy_rate=buy_rate,
                        sell_rate=sell_rate
                    )
                    self.stdout.write(self.style.SUCCESS(f'New rate stored for {rate_type}.'))
                else:
                    self.stdout.write(self.style.WARNING(f'No change for {rate_type}, no new record added.'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An error occurred: {str(e)}"))
