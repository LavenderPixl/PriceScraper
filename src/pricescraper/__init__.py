from itertools import product

from bs4 import BeautifulSoup
import os.path
import requests
import csv

file_name = "ProshopProducts.csv"


# Create a CSV file if it does not already exist.
def startup_csv():
    if not os.path.isfile(file_name):
        with open(file_name, 'w') as csv_file:
            writer = csv.writer(csv_file, delimiter=' ')
            writer.writerow(["Name", "Price"])


# Get HTML belonging to the URL.
def get_html(url):
    html = requests.get(url)
    if html.status_code != 200:
        print("Error getting html from", url)
        print(f"Status code: {html.status_code}")
        exit(1)
    else:
        return BeautifulSoup(html.content, "html.parser")


def get_products(sp: BeautifulSoup):
    products = []
    for child_soup in sp.find_all("ul", {"id": "product-list"}):
        title = child_soup.find('h2').text
        price = child_soup.find('span').text

        products.append([title, price])
    return products


def write_to_csv(sp: list[list[str]]):
    with open(file_name, 'w') as csv_file:
        fieldnames = ['Name', 'Price']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(sp)

startup_csv()
soup = get_html("https://www.scrapingcourse.com/ecommerce/")
products = get_products(soup)
write_to_csv(products)