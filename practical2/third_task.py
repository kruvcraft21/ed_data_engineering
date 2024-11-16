# Агрегируйте информацию по каждому товару, получив
# следующую информацию: средняя цена, максимальная цена, минимальная цена.

import json
import msgpack
import os

with open("third_task.json", 'r') as json_file:
    data = json.load(json_file)

agg_data = {}

for element in data:
    if element['name'] in agg_data:
        agg_data[element['name']].append(element['price'])
    else:
        agg_data[element['name']] = []
        agg_data[element['name']].append(element['price'])

result = {}
for name, arr in agg_data.items():
    result[name] = {
        'avg': sum(arr) / len(arr),
        'max': max(arr),
        'min': min(arr)
    }

# Сохранить полученную информацию по каждому объекту в
# формате json, а также в формате msgpack. Сравните размеры полученных файлов.

with open("third_task_result.json", 'w', encoding='utf-8') as json_file:
    json.dump(result, json_file, indent=4, ensure_ascii=False)

with open("third_task_result.msgpack", 'wb') as msgpack_file:
    msgpack.dump(result, msgpack_file)

json_size = os.path.getsize("third_task_result.json")
msgpack_size = os.path.getsize("third_task_result.msgpack")
print(f"Разница в размерах {json_size / msgpack_size}")
# Разница в размерах 2.1810253137630293