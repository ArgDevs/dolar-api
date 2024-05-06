import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand

from rates.models import ExchangeRate
from rates.scraper import scrape_exchange_rates


class Command(BaseCommand):
    help = 'Scrapes exchange rates and stores them in the database'

    def handle(self, *args, **options):
        self.stdout.write("Starting to scrape exchange rates...")

        try:
            url = 'https://dolarhoy.com/'
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            rates = scrape_exchange_rates(soup)

            for rate_type, rate_info in rates.items():
                ExchangeRate.objects.create(
                    rate_type=rate_type,
                    origin_currency='USD',
                    exchange_currency='ARS',
                    buy_rate=rate_info['Compra'] if rate_info['Compra'] != 'N/A' else -1,
                    sell_rate=rate_info['Venta'] if rate_info['Venta'] != 'N/A' else -1
                )

            self.stdout.write(self.style.SUCCESS('Successfully stored exchange rates.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An error occurred: {str(e)}"))
