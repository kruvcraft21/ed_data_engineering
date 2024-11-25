import glob
from bs4 import BeautifulSoup
import pandas as pd
import json


def parse_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    # Извлечение данных
    product_data = {}
    product_data['article'] = soup.find('h1', class_='title')['id']
    product_data['name'] = soup.find('h1', class_='title').text.split(':')[-1].strip()
    product_data['city'] = soup.find('p', class_='address-price').text.split('Город:')[-1].split('Цена')[0].strip()
    product_data['price'] = int(soup.find('p', class_='address-price').text.split('Цена:')[-1].strip().split()[0])
    product_data['color'] = soup.find('span', class_='color').text.split(':')[-1].strip()
    product_data['quantity'] = int(soup.find('span', class_='quantity').text.split(':')[-1].strip().split()[0])
    product_data['rating'] = float(soup.find('span', string=lambda x: x and "Рейтинг" in x).text.split(':')[-1].strip())
    product_data['views'] = int(soup.find('span', string=lambda x: x and "Просмотры" in x).text.split(':')[-1].strip())

    # Добавление поля "Наличие"
    availability_text = soup.find('span', string=lambda x: x and "Наличие" in x).text.split(':')[-1].strip()
    product_data['availability'] = availability_text == "Да"  # Преобразуем в логическое значение

    img = soup.find('img')
    if img:
        product_data['image'] = img['src']

    return product_data


data = [parse_html(file) for file in glob.glob('1/*.html')]

df = pd.DataFrame(data)

df.to_json("first_task.json", orient='records', force_ascii=False)

df_sorted = df.sort_values(by=['views'], ascending=False)

df_sorted.to_json("first_task_sorted.json", orient='records', force_ascii=False)

df_filter = df[df['availability']]

df_filter.to_json('first_task_filter.json', orient='records', force_ascii=False)

df_stat = {
    'count': float(df['price'].count()),
    'min': float(df['price'].min()),
    'max': float(df['price'].max()),
    'sum': float(df['price'].sum()),
    'mean': float(df['price'].mean()),
}

with open('first_task_stats.json', 'w', encoding='utf-8') as file:
    json.dump(df_stat, file, ensure_ascii=False)

df_text_freq = df['color'].value_counts().to_dict()

with open('first_task_text_freq.json', 'w', encoding='utf-8') as file:
    json.dump(df_text_freq, file, ensure_ascii=False)
