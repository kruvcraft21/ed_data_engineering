from lxml import etree
import pandas as pd
import glob, json


def parse_xml(xml_file):
    tree = etree.parse(xml_file)
    root = tree.getroot()

    items = []
    for clothing in root.findall('clothing'):
        item = {'exclusive': False, 'sporty': False, 'new': False}
        for param in clothing.getchildren():
            if param.tag in ['exclusive', 'sporty']:
                item[param.tag] = True if param.text.strip() == 'yes' else False
            elif param.tag == 'new':
                item[param.tag] = True if param.text.strip() == '+' else False
            elif param.tag == 'id' :
                item[param.tag] = int(param.text.strip())
            elif param.tag in ['price', 'rating', 'reviews']:
                item[param.tag] = float(param.text.strip())
            else:
                item[param.tag] = param.text.strip()
        items.append(item)
    return items

df = pd.DataFrame(columns=['id', 'name', 'category', 'size', 'color',
       'material', 'price', 'rating', 'reviews', 'exclusive', 'sporty', 'new'])

for file in glob.glob('4/*.xml'):
    products = pd.DataFrame(parse_xml(file))
    df = pd.concat([df if not df.empty else None, products])

df.to_json('fourth_task.json', orient='records', force_ascii=False)

df_sorted = df.sort_values(by=['rating'], ascending=False)

df_sorted.to_json('fourth_task_sorted.json', orient='records', force_ascii=False)

df_filtered = df[df['new']]

df_filtered.to_json('fourth_task_filtered.json', orient='records', force_ascii=False)

df_stat = {
    'count': float(df['price'].count()),
    'min': float(df['price'].min()),
    'max': float(df['price'].max()),
    'sum': float(df['price'].sum()),
    'mean': float(df['price'].mean()),
}

with open('fourth_task_stats.json', 'w', encoding='utf-8') as file:
    json.dump(df_stat, file, ensure_ascii=False)

df_text_freq = df['material'].value_counts().to_dict()

with open('fourth_task_text_freq.json', 'w', encoding='utf-8') as file:
    json.dump(df_text_freq, file, ensure_ascii=False)