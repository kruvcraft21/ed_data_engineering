import glob
from bs4 import BeautifulSoup
import pandas as pd
import json
import re

def parse_html(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    products = []
    product_items = soup.find_all("div", class_="product-item")
    for item in product_items:
        product = {}
        product["id"] = item.find("a", class_="add-to-favorite")["data-id"]
        product["name"] = item.find("span").text.strip()
        product["price"] = int(re.sub(r"\D", "", item.find("price").text.strip()))
        product["bonus"] = int(re.sub(r"\D", "", item.find("strong").text.strip()))

        # Извлечение характеристик
        product["specs"] = {}
        for spec in item.find_all("li"):
            key = spec["type"]
            value = spec.text.strip()
            if "ГГц" in value or "мА * ч" in value or "MP" in value or "GB" in value:
                value = re.sub(r"[^\d.]", "", value)
                value = float(value) if "." in value else int(value)
            product["specs"][key] = value

        img = item.find("img")
        if img:
            product["image"] = img["src"]

        products.append(product)
    return products

df = pd.DataFrame(columns=["id", "name", "price", "bonus", "specs", "image"])

for html_file in glob.glob("2/*.html"):
    products = pd.DataFrame(parse_html(html_file))
    df = pd.concat([df if not df.empty else None, products])

df.to_json("second_task.json", orient='records', force_ascii=False)

df_sorted = df.sort_values(by=['bonus'], ascending=False)

df_sorted.to_json("second_task_sorted.json", orient='records', force_ascii=False)

df_filter = df[df['price'] < 257251]

df_filter.to_json('second_task_filter.json', orient='records', force_ascii=False)

df_stat = {
    'count': float(df['price'].count()),
    'min': float(df['price'].min()),
    'max': float(df['price'].max()),
    'sum': float(df['price'].sum()),
    'mean': float(df['price'].mean()),
}

with open('second_task_stats.json', 'w', encoding='utf-8') as file:
    json.dump(df_stat, file, ensure_ascii=False)

df_text_freq = df['name'].value_counts().to_dict()

with open('second_task_text_freq.json', 'w', encoding='utf-8') as file:
    json.dump(df_text_freq, file, ensure_ascii=False)
