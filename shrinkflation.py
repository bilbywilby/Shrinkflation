import csv
import os
import pickle
from typing import Tuple

import requests
from bs4 import BeautifulSoup
import configparser
from product import Product, parse_sites
from shrinkflation import detect_shrinkflation

CACHE_FILE = 'product_cache.pkl'

config = configparser.ConfigParser()
config.read('config.ini')

if 'DEFAULT' in config and 'Database' in config['DEFAULT']:
    DATABASE = config['DEFAULT']['Database']
else:
    # handle the case where the 'Database' key is missing
    DATABASE = 'default_database_name'


def get_product_info(product_url: str) -> Tuple[float, float]:
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'rb') as file:
            cache = pickle.load(file)
    else:
        cache = {}

    if product_url in cache:
        return cache[product_url]

    response = requests.get(product_url)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')

    size_element = soup.find('span', {'class': 'size'})
    if size_element is None:
        size = 0
    else:
        size = float(size_element.text.strip().replace('oz', ''))

    price_element = soup.find('span', {'class': 'price'})
    if price_element is None:
        price = 0
    else:
        price = float(price_element.text.strip().replace('$', ''))

    result = (size, price)
    cache[product_url] = result

    with open(CACHE_FILE, 'wb') as file:
        pickle.dump(cache, file)

    return result


def write_results(product_pairs):
    with open('results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Old Product', 'New Product',
                        'Shrinkflation Detected'])

        for old_product, new_product in product_pairs:
            is_shrinkflation = detect_shrinkflation(old_product, new_product)
            writer.writerow([old_product, new_product, is_shrinkflation])


if __name__ == '__main__':
    top_products = parse_sites()
    print("\nTop 5 products based on price and weight:")
    for i, product in enumerate(sorted(top_products, key=lambda x: (x.price, x.size)), start=1):
        print(f"{i}. {product}")

    product_pairs = [
        ('https://example.com/product1/old', 'https://example.com/product1/new'),
        ('https://example.com/product2/old', 'https://example.com/product2/new'),
        ('https://example.com/product3/old', 'https://example.com/product3/new'),
    ]

    write_results(product_pairs)
product.py:  # type: ignore


class Product:
    def __init__(self, url):
        self.url = url
        self.name = ""
        self.size = 0
        self.price = 0
        self.units = ""

    def __str__(self):
        return f"{self.name} ({self.size} {self.units}) - ${self.price}"

    def parse_product_info(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, "html.parser")

        name_element = soup.find("h1", class_="product-name")
        if name_element:
            self.name = name_element.text.strip()

        size_element = soup.find("span", class_="product-weight")
        self.units = "oz"
        if not size_element:
            size_element = soup.find("span", class_="product-size")
            self.units = size_element.find_next_sibling("span").text.strip()
        self.size = float(size_element.text.strip().replace(self.units, ""))

        price_element = soup.find("span", class_="product-sales-price")
        if not price_element:
            price_element = soup.find("span", class_="product-price")
        self.price = float(price_element.text.strip().replace("$", ""))
        self.name = soup.find("h1", class_="product-name").text.strip()

        size_element = soup.find("span", class_="product-weight")
        self.units = "oz"
        if not size_element:
            size_element = soup.find("span", class_="product-size")
            self.units = size_element.find_next_sibling("span").text.strip()
        self.size = float(size_element.text.strip().replace(self.units, ""))


def detect_shrinkflation(old_product: str, new_product: str, price_unit: str = 'USD',
                         size_unit: str = 'oz') -> bool:
    try:
        old_size, old_price = get_product_info(old_product)
        new_size, new_price = get_product_info(new_product)

        factor_dict = {
            'USD': 1,
            'EUR': 0.85,
            'GBP': 0.72
        }
        price_factor = factor_dict.get(price_unit, None)
        if price_factor is None:
            raise ValueError('Invalid price unit')

        factor_dict = {
            'oz': 1,
            'g': 0.035
        }
        size_factor = factor_dict.get(size_unit, None)
        if size_factor is None:
            raise ValueError('Invalid size unit')

        old_value = old_size * old_price * size_factor * price_factor
        new_value = new_size * new_price * size_factor * price_factor

        return old_value > new_value

    except Exception as e:
        print(f'Error detecting shrinkflation for products  "{old_product}" and "{new_product}":\n{e}')
        return False     
    if __name__ == '__main__':
        import doctest
        doctest.testmod() < new_func()


def new_func():
    return / >
