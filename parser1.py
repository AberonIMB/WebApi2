import requests
from bs4 import BeautifulSoup

base_url = 'https://www.maxidom.ru/catalog/praga/'

def parse_page(url):
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')
    items = []

    products = soup.find_all('article', class_='l-product')

    for product in products:
        name = product.find('span', itemprop='name')
        price = product.find('div', class_='l-product__price-base')

        items.append((name.text.strip(), price.text.strip()))

    next_page_button = soup.find('a', id='navigation_2_next_page')

    if next_page_button:
        next_page_url = next_page_button['href']
        next_page_url = "https://www.maxidom.ru" + next_page_url
    else:
        next_page_url = None

    return items, next_page_url

def parse_all_pages():
    url = base_url
    all_items = []

    while url:
        items, url = parse_page(url)
        all_items.extend(items)

    print("Продукты получены")
    return all_items

# products = parse_all_pages()
# for product in products:
#     print(f"Наименование товара: {product[0]}, цена: {product[1]}")
# print(len(products))