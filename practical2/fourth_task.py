import pickle
import json

def update_prices(data, updates):
    for update in updates:
        for product in data:
            if product['name'] == update['name']:
                if update['method'] == 'add':
                    product['price'] += update['param']
                elif update['method'] == 'sub':
                    product['price'] -= update['param']
                elif update['method'] == 'percent+':
                    product['price'] += (product['price'] * update['param'])
                elif update['method'] == 'percent-':
                    product['price'] -= (product['price'] * update['param'])

with open('fourth_task_products.json', 'rb') as f:
    products = pickle.load(f)

with open('fourth_task_updates.json', 'r') as f:
    price_updates = json.load(f)

update_prices(products, price_updates)

with open('fourth_task_result.pkl', 'wb') as f:
    pickle.dump(products, f)
