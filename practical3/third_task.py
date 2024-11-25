import pandas as pd
from lxml import etree
import re, glob, json


def convert_to_number(value):
    match = re.search(r"[-+]?\d*\.\d+|\d+", value)
    if match:
        return float(match.group(0))
    return value


def parse_xml(file_path):
    tree = etree.parse(file_path)
    root = tree.getroot()

    # Преобразование XML в словарь
    data = {}
    for child in root:
        if not child.tag in ['name', 'constellation', 'spectral-class']:
            data[child.tag] = convert_to_number(child.text)
        else:
            data[child.tag] = child.text.strip()
    return data


raw_df = [parse_xml(file) for file in glob.glob("3/*.xml")]

df = pd.DataFrame(raw_df)

df.to_json("third_task.json", orient='records', force_ascii=False)

df_sorted = df.sort_values(by=['distance'], ascending=False)

df_sorted.to_json("third_task_sorted.json", orient='records', force_ascii=False)

mean_radius = 512909132

df_filter = df[df['radius'] > mean_radius]

df_filter.to_json('third_task_filter.json', orient='records', force_ascii=False)

df_stat = {
    'count': float(df['age'].count()),
    'min': float(df['age'].min()),
    'max': float(df['age'].max()),
    'sum': float(df['age'].sum()),
    'mean': float(df['age'].mean()),
}

with open('third_task_stats.json', 'w', encoding='utf-8') as file:
    json.dump(df_stat, file, ensure_ascii=False)

df_text_freq = df['spectral-class'].value_counts().to_dict()

with open('third_task_text_freq.json', 'w', encoding='utf-8') as file:
    json.dump(df_text_freq, file, ensure_ascii=False)
