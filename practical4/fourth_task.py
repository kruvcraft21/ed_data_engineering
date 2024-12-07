import json
import sqlite3
import pandas as pd

def write_counter(file_name, list_tuples):
    with open(file_name, 'w') as file:
        for key, value in list_tuples:
            file.write(f"{key}:{value}\n")

def write_list(file_name, list):
    with open(file_name, "w") as file:
        for item in list:
            file.write(str(item) + "\n")

def get_dict_from_exec(cursor):
    return [dict(zip([desc[0] for desc in cursor.description], row)) for row in cursor.fetchall()]

df_products = pd.read_json("4/_product_data.json")

with sqlite3.connect("fourth_task.db") as conn:
    cursor = conn.cursor()

    # Создание таблицы
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            price REAL NOT NULL CHECK (price >= 0),
            quantity INTEGER NOT NULL CHECK (quantity >= 0),
            category TEXT,
            from_city TEXT,
            is_available BOOLEAN,
            views INTEGER NOT NULL CHECK (views >= 0),
            update_count INTEGER DEFAULT 0
        )
        """)
    conn.commit()

    for index, product in df_products.iterrows():
        cursor.execute("""
            INSERT OR IGNORE INTO products (name, price, quantity, category, from_city, is_available, views)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
            product["name"], product["price"], product["quantity"],
            product["category"], product["fromCity"], product["isAvailable"], product["views"]
        ))
    conn.commit()

    df_upd = pd.read_csv("4/_update_data.csv", sep=';')

    for index, update in df_upd.iterrows():
        name, method, param = update["name"], update["method"], update["param"]
        cursor.execute("SELECT * FROM products WHERE name = ?", (name,))
        products = cursor.fetchall()
        if not products:
            print(f"Product {name} not found.")
            continue

        for product in products:
            cursor.execute("BEGIN TRANSACTION")
            if method == "price_abs":
                new_price = max(0., product[2] + float(param))
                cursor.execute("UPDATE products SET price = ?, update_count = update_count + 1 WHERE name = ?",
                               (new_price, name))
            elif method == "price_percent":
                new_price = max(0., product[2] + (product[2] * float(param)))
                cursor.execute("UPDATE products SET price = ?, update_count = update_count + 1 WHERE name = ?",
                               (new_price, name))
            elif method == "quantity_add":
                new_quantity = product[3] + int(param)
                cursor.execute("UPDATE products SET quantity = ?, update_count = update_count + 1 WHERE name = ?",
                               (new_quantity, name))
            elif method == "quantity_sub":
                new_quantity = max(0, product[3] - int(param))
                cursor.execute("UPDATE products SET quantity = ?, update_count = update_count + 1 WHERE name = ?",
                               (new_quantity, name))
            elif method == "available":
                cursor.execute("UPDATE products SET is_available = ?, update_count = update_count + 1 WHERE name = ?",
                               (bool(param), name))
            elif method == "remove":
                cursor.execute("DELETE FROM products WHERE name = ?", (name,))
            cursor.execute("COMMIT")

    conn.commit()

    freq = cursor.execute("""
        SELECT name, update_count FROM products
        ORDER BY update_count DESC
        LIMIT 10
        """).fetchall()
    print(freq)

    write_counter("fourth_task_freq.txt", freq)

    cursor.execute("""
        SELECT category, 
               SUM(price) AS total_price, 
               MIN(price) AS min_price, 
               MAX(price) AS max_price, 
               AVG(price) AS avg_price,
               COUNT(*) AS product_count
        FROM products
        GROUP BY category
        """)
    price_stat = get_dict_from_exec(cursor)
    print("Price analysis:")
    print(price_stat)
    with open("fourth_task_category_price_stat.json", "w") as file:
        json.dump(price_stat, file, ensure_ascii=False, indent=4)

    cursor.execute("""
        SELECT category, 
               SUM(quantity) AS total_quantity, 
               MIN(quantity) AS min_quantity, 
               MAX(quantity) AS max_quantity, 
               AVG(quantity) AS avg_quantity
        FROM products
        GROUP BY category
        """)
    quantity_stat = get_dict_from_exec(cursor)
    print("Quantity analysis:")
    print(quantity_stat)
    with open("fourth_task_quantity_stat.json", "w") as file:
        json.dump(quantity_stat, file, ensure_ascii=False, indent=4)

    cursor.execute("""
        SELECT name, price, quantity 
        FROM products
        WHERE views > 10000
        """)
    custom_query = get_dict_from_exec(cursor)
    print("Custom query:")
    print(custom_query)
    with open("fourth_task_custom_query.json", "w") as file:
        json.dump(custom_query, file, ensure_ascii=False, indent=4)
