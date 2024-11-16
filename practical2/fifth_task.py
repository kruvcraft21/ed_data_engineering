# Источник данных
# https://www.kaggle.com/datasets/safrin03/predictive-analytics-for-customer-churn-dataset

import pandas as pd
import json
import os
import msgpack

df = pd.read_csv('train.csv')

# Выбор 7-10 полей для дальнейшей работы
selected_columns = [
    'MonthlyCharges', 'TotalCharges', 'ViewingHoursPerWeek',
    'AverageViewingDuration', 'ContentDownloadsPerMonth',
    'SubscriptionType', 'PaymentMethod', 'Churn', 'GenrePreference'
]
df_selected = df[selected_columns]

# Расчёт статистик для числовых полей
numerical_columns = df_selected.select_dtypes(include='number').columns
stats = df_selected[numerical_columns].agg(['max', 'min', 'mean', 'sum', 'std']).to_dict()


# Расчёт частоты для категориальных полей
categorical_columns = df_selected.select_dtypes(include='object').columns
for column in categorical_columns:
    stats[column] = df_selected[column].value_counts().to_dict()

with open('fifth_task_stat.json', 'w') as json_file:
    json.dump(stats, json_file, indent=4)

df_selected.to_csv('fifth_task_result.csv', index=False)
df_selected.to_json('fifth_task_result.json', orient='records')
df_selected.to_pickle('fifth_task_result.pkl')
with open('fifth_task_result.msgpack', 'wb') as f:
    msgpack.dump(df_selected.to_dict(orient='records'), f)

print(f"Размер CSV с выбранными данными {os.path.getsize('fifth_task_result.csv')}")
print(f"Размер JSON с выбранными данными {os.path.getsize('fifth_task_result.json')}")
print(f"Размер PKL с выбранными данными {os.path.getsize('fifth_task_result.pkl')}")
print(f"Размер MSGPACK с выбранными данными {os.path.getsize('fifth_task_result.msgpack')}")
# Размер CSV с выбранными данными 26041383
# Размер JSON с выбранными данными 64630623
# Размер PKL с выбранными данными 13168120
# Размер MSGPACK с выбранными данными 52823153
