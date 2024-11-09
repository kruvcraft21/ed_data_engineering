import pandas as pd

df = pd.read_csv('fourth_task.txt')
df = df.drop('category', axis=1)

avg_rating = df['rating'].mean()
max_quantity = df['quantity'].max()
min_price = df['price'].min()

with open('fourth_task_result_values.txt', 'w', encoding='utf-8') as file:
    for value in [avg_rating, max_quantity, min_price]:
        file.write(f'{value}\n')

df = df[df['price'] < 4194]
df.to_csv('fourth_task_result.csv', index=False)