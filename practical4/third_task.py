import pandas as pd
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

df_csv = pd.read_csv("3/_part_1.csv", delimiter=";")

custom_data = []
with open("3/_part_2.text", "r", encoding="utf-8") as file:
    raw_data = file.read()
    records = raw_data.split("=====\n")
    for record in records:
        if len(record) > 0:
            record_dict = {}
            for line in record.strip().split("\n"):
                key, value = line.strip().split("::")
                record_dict[key] = value

            custom_data.append(record_dict)

df_custom = pd.DataFrame(custom_data)

common_columns = ['artist', 'song', 'duration_ms', 'year', 'tempo', 'genre', 'loudness']
df_csv = df_csv[common_columns]
df_custom = df_custom[common_columns]

df_custom['duration_ms'] = df_custom['duration_ms'].astype(int)
df_custom['year'] = df_custom['year'].astype(int)
df_custom['tempo'] = df_custom['tempo'].astype(float)
df_custom['loudness'] = df_custom['loudness'].astype(float)

df_merged = pd.concat([df_csv, df_custom], ignore_index=True)

with sqlite3.connect("third_task.db") as conn:
    df_merged.to_sql('music', conn, if_exists='replace', index=False)
    cursor = conn.cursor()

    VAR = 77

    cursor.execute(f'''
    SELECT * FROM music ORDER BY duration_ms LIMIT {VAR + 10}
    ''')
    rows = cursor.fetchall()
    with open('third_task_sorted.json', 'w', encoding='utf-8') as file:
        json.dump([dict(zip([column[0] for column in cursor.description], row)) for row in rows], file,
                  ensure_ascii=False)

    stats_query = """
    SELECT SUM(duration_ms) AS total, 
           MIN(duration_ms) AS min, 
           MAX(duration_ms) AS max, 
           AVG(duration_ms) AS average
    FROM music
    """
    stats_result = cursor.execute(stats_query).fetchone()
    print(f"Сумма: {stats_result[0]}, Мин: {stats_result[1]}, Макс: {stats_result[2]}, Среднее: {stats_result[3]}")

    write_list("third_task_stat.txt", stats_result)

    freq_query = """
    SELECT music.artist, COUNT(*) as freq
    FROM music
    GROUP BY artist
    ORDER BY freq DESC 
    """
    freq_result = cursor.execute(freq_query).fetchall()
    print("Частота значений поля 'artist':")
    for row in freq_result:
        print(f"{row[0]}: {row[1]}")
    write_counter("third_task_freq.txt", freq_result)

    filtered_query = f"""
    SELECT * FROM music 
    WHERE tempo > 100 
    ORDER BY duration_ms DESC 
    LIMIT {VAR + 15}
    """

    filtered_data = cursor.execute(filtered_query).fetchall()
    with open("third_task_filtered.json", "w", encoding="utf-8") as f:
        json.dump([dict(zip([desc[0] for desc in cursor.description], row)) for row in filtered_data], f,
                  ensure_ascii=False, indent=4)

