import logging

import requests
from bs4 import BeautifulSoup


def get_html(url):
    response = requests.get(url)
    response.raise_for_status()  # Ensures HTTP errors are caught
    return response.text


def parse_html(html):
    return BeautifulSoup(html, 'html.parser')


def scrape_exchange_rates(soup):
    rates = {}
    rate_tiles = soup.find_all('div', class_='tile is-child')

    for tile in rate_tiles:
        title_tag = tile.find('a', class_='title')
        if not title_tag:
            continue

        rate_type = title_tag.text.strip()
        values_div = tile.find('div', class_='values')
        if not values_div:
            continue

        compra_div = values_div.find('div', class_='compra')
        compra_val = 'N/A'
        if compra_div:
            compra_val_tag = compra_div.find('div', class_='val')
            if compra_val_tag:
                compra_val = compra_val_tag.text.strip()
            else:
                logging.warning(f"Compra value missing for {rate_type}.")
        else:
            logging.warning(f"Compra div missing for {rate_type}.")

        venta_div = values_div.find('div', class_='venta')
        venta_val = 'N/A'
        if venta_div:
            venta_val_tag = venta_div.find('div', class_='val')
            if venta_val_tag:
                venta_val = venta_val_tag.text.strip()
            else:
                logging.warning(f"Venta value missing for {rate_type}.")
        else:
            logging.warning(f"Venta div missing for {rate_type}.")

        rates[rate_type] = {
            'Compra': compra_val.replace('$', ''),
            'Venta': venta_val.replace('$', '')
        }
        logging.info(f"Scraped rates for {rate_type}: Compra - {compra_val}, Venta - {venta_val}")

    return rates


def main():
    url = 'https://dolarhoy.com/'
    logging.info("Starting to scrape the website.")
    try:
        html = get_html(url)
        soup = parse_html(html)
        rates = scrape_exchange_rates(soup)
        print(rates)
        logging.info("Scraping completed successfully.")
    except Exception as e:
        logging.exception("Failed to scrape due to an error.")
        raise


if __name__ == "__main__":
    main()
