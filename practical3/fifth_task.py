# Самостоятельно найти сайт, соответствующий следующим условиям:
#     • непопулярный, регионального уровня или из узкой области (с целью избежать дублирования)
#     • наличие страниц-каталогов, где есть информация сразу по нескольких объектам
#     • наличие страниц, посвященных отдельному объекту

# Необходимо:
#     • спарсить страницы-каталоги, где размещена информация сразу по нескольким объектам.

from bs4 import BeautifulSoup
import requests, re, json
import pandas as pd

catalogs = ["https://ameot.ru/pod_zakaz",
            "https://ameot.ru/pod_zakaz?page=2",
            "https://ameot.ru/locker",
            "https://ameot.ru/locker?page=2"
            "https://ameot.ru/table",
            "https://ameot.ru/table?page=2",
            "https://ameot.ru/living-room"]

def get_numbers(s) -> list:
    return re.findall(r'\d+', s)

def parse_catalog(catalog_url: str):
    r = requests.get(catalog_url)
    soup = BeautifulSoup(r.text, "lxml")
    items = []
    type = soup.find('h1').text.strip()
    for product in soup.find_all("div", {"class": "product-thumb"}):
        item = {}
        price = product.find_all('p', {'class': 'price'})[0].text.strip()
        prices = get_numbers(price)
        if len(prices) > 1:
            item['price_new'] = int(prices[0])
            item['price_old'] = int(prices[1])
        else:
            item['price_new'] = int(prices[0])
            item['price_old'] = int(prices[0])

        item['image_src'] = product.find('img')['src']
        item['link_to_product'] = product.find('a')['href']
        item['description'] = product.find('h4').text.strip()
        item['type'] = type
        item['is_new'] = False
        item['discount'] = 0

        diamont_st = product.find('span', {'class': 'diamont_st'})
        if diamont_st is not None:
            diamont_text = diamont_st.text.strip()
            item['is_new'] = True if 'new' in diamont_text else False
            discount = get_numbers(diamont_text)
            item['discount'] = int(discount[0]) if len(discount) > 0 else 0

        item['rating'] = len(product.find_all('i', {'class': 'fa fa-star fa-stack-2x'}))

        items.append(item)

    return items

def parse_product(product_url: str):
    r = requests.get(product_url)
    soup = BeautifulSoup(r.text, "lxml")

    product = {}
    product['name'] = soup.find('h1', {'class': 'pr-name'}).text.strip()
    product['manufacturer'] = soup.find('a', {'itemprop':"manufacturer"}).text.strip()
    price_new = get_numbers(soup.find('span', {'class':"priceproduct-new"}).text.strip())
    product['price_new'] = int(price_new[0])
    price_old = soup.find('span', {'class':"priceproduct-old"})
    if price_old is None:
        product['price_old'] = int(price_new[0])
    else:
        price_old_number = get_numbers(price_old.text.strip())
        product['price_old'] = int(price_old_number[0])

    product['is_new'] = False
    product['discount'] = 0

    diamont_st = soup.find('span', {'class': 'diamont_st'})
    if diamont_st is not None:
        diamont_text = diamont_st.text.strip()
        product['is_new'] = True if 'new' in diamont_text else False
        discount = get_numbers(diamont_text)
        product['discount'] = int(discount[0]) if len(discount) > 0 else 0

    reviews = soup.find('a', {'class': 'review_profile'}).text.strip()
    review_count = get_numbers(reviews)
    product['review_count'] = int(review_count[0]) if len(review_count) > 0 else 0
    product['rating'] = len(soup.find_all('i', {'class': 'fa fa-star fa-stack-2x'}))

    product['image_url'] = soup.find('img', {'id': 'main-image'})['src']

    return product

df_catalogs = pd.DataFrame(columns=['price_new', 'price_old', 'image_src', 'link_to_product', 'description',
       'is_new', 'discount', 'rating', 'type'])

for catalog in catalogs:
    items_dict = pd.DataFrame(parse_catalog(catalog))
    df_catalogs = pd.concat([df_catalogs if not df_catalogs.empty else None, items_dict])

df_catalogs.to_json('fifth_task_catalogs.json', orient='records', force_ascii=False)

df_catalogs_sorted = df_catalogs.sort_values('rating', ascending=False)

df_catalogs_sorted.to_json('fifth_task_catalogs_sorted.json', orient='records', force_ascii=False)

df_catalogs_filtered = df_catalogs[df_catalogs['is_new']]

df_catalogs_filtered.to_json('fifth_task_catalogs_filtered.json', orient='records', force_ascii=False)

df_catalogs_stat = {
    'count': float(df_catalogs['price_new'].count()),
    'min': float(df_catalogs['price_new'].min()),
    'max': float(df_catalogs['price_new'].max()),
    'sum': float(df_catalogs['price_new'].sum()),
    'mean': float(df_catalogs['price_new'].mean()),
}

with open('fifth_task_catalogs_stat.json', 'w', encoding='utf-8') as file:
    json.dump(df_catalogs_stat, file, ensure_ascii=False)

df_text_freq = df_catalogs['description'].value_counts().to_dict()

with open('fifth_task_catalogs_text_freq.json', 'w', encoding='utf-8') as file:
    json.dump(df_text_freq, file, ensure_ascii=False)

# Необходимо:
#     • спарсить нескольких страниц (минимум 10), посвященных только одному объекту;
#

products = df_catalogs.sample(20)['link_to_product'].values

products_list = [parse_product(product_url) for product_url in products]

df_products = pd.DataFrame(products_list)

df_products.to_json('fifth_task_products.json', orient='records', force_ascii=False)

df_products_sorted = df_products.sort_values('review_count', ascending=False)

df_products_sorted.to_json('fifth_task_products_sorted.json', orient='records', force_ascii=False)

df_products_filtered = df_products[df_products['is_new']]

df_products_filtered.to_json('fifth_task_products_filtered.json', orient='records', force_ascii=False)

df_products_stat = {
    'count': float(df_products['price_old'].count()),
    'min': float(df_products['price_old'].min()),
    'max': float(df_products['price_old'].max()),
    'sum': float(df_products['price_old'].sum()),
    'mean': float(df_products['price_old'].mean()),
}

with open('fifth_task_products_stat.json', 'w', encoding='utf-8') as file:
    json.dump(df_products_stat, file, ensure_ascii=False)

df_products_text_freq = df_products['manufacturer'].value_counts().to_dict()

with open('fifth_task_products_text_freq.json', 'w', encoding='utf-8') as file:
    json.dump(df_products_text_freq, file, ensure_ascii=False)