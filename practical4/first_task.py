import sqlite3
import json

def write_counter(file_name, list_tuples):
    with open(file_name, 'w') as file:
        for key, value in list_tuples:
            file.write(f"{key}:{value}\n")

def write_list(file_name, list):
    with open(file_name, "w") as file:
        for item in list:
            file.write(str(item) + "\n")

with open("1-2/item.text", "r", encoding="utf-8") as file:
    raw_data = file.read()

records = raw_data.split("=====\n")
data = []
for record in records:
    if len(record) > 0:
        record_dict = {}
        for line in record.strip().split("\n"):
            key, value = line.strip().split("::")
            record_dict[key] = value

        data.append(record_dict)

conn = sqlite3.connect("first_second_task.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS tournaments (
    id INTEGER PRIMARY KEY,
    name TEXT,
    city TEXT,
    begin TEXT,
    system TEXT,
    tours_count INTEGER,
    min_rating INTEGER,
    time_on_game INTEGER
)
""")
conn.commit()

for record in data:
    cursor.execute("""
    INSERT OR IGNORE INTO tournaments (id, name, city, begin, system, tours_count, min_rating, time_on_game)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        int(record["id"]),
        record["name"],
        record["city"],
        record["begin"],
        record["system"],
        int(record["tours_count"]),
        int(record["min_rating"]),
        int(record["time_on_game"])
    ))
conn.commit()

VAR = 77

sorted_query = f"""
SELECT * FROM tournaments ORDER BY min_rating DESC LIMIT {VAR + 10}
"""
sorted_data = cursor.execute(sorted_query).fetchall()
with open("first_task_sorted.json", "w", encoding="utf-8") as f:
    json.dump([dict(zip([desc[0] for desc in cursor.description], row)) for row in sorted_data], f, ensure_ascii=False, indent=4)

stats_query = """
SELECT SUM(time_on_game) AS total, 
       MIN(time_on_game) AS min, 
       MAX(time_on_game) AS max, 
       AVG(time_on_game) AS average
FROM tournaments
"""
stats_result = cursor.execute(stats_query).fetchone()
print(f"Сумма: {stats_result[0]}, Мин: {stats_result[1]}, Макс: {stats_result[2]}, Среднее: {stats_result[3]}")

write_list("first_task_stat.txt", stats_result)

freq_query = """
SELECT system, COUNT(*) AS frequency
FROM tournaments
GROUP BY system
ORDER BY frequency DESC
"""
freq_result = cursor.execute(freq_query).fetchall()
print("Частота значений поля 'system':")
for row in freq_result:
    print(f"{row[0]}: {row[1]}")
write_counter("first_task_freq.txt", freq_result)

filtered_query = f"""
SELECT * FROM tournaments WHERE min_rating > 2400 ORDER BY min_rating DESC LIMIT {VAR + 10}
"""
filtered_data = cursor.execute(filtered_query).fetchall()
with open("first_task_filtered.json", "w", encoding="utf-8") as f:
    json.dump([dict(zip([desc[0] for desc in cursor.description], row)) for row in filtered_data], f, ensure_ascii=False, indent=4)

conn.close()