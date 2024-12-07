import msgpack
import sqlite3
import json

with open("1-2/subitem.msgpack", 'rb') as f:
    tournament_results = msgpack.unpackb(f.read())

with sqlite3.connect("first_second_task.db") as conn:
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tournament_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        place INTEGER,
        prise INTEGER,
        FOREIGN KEY (name) REFERENCES tournaments(name)
    )
    """)
    conn.commit()

    for result in tournament_results:
        cursor.execute("""
        INSERT OR IGNORE INTO tournament_results (name, place, prise)
        VALUES (?, ?, ?)
        """, (result["name"], result["place"], result["prise"]))
    conn.commit()

    query1 = """
    SELECT tr.name, tr.place, tr.prise, t.city, t.system
    FROM tournament_results AS tr
    JOIN tournaments AS t ON tr.name = t.name
    """
    result1 = cursor.execute(query1).fetchall()
    print("Запрос 1: Турниры с местами и призовыми:")
    for row in result1:
        print(row)

    query1_json = [
        {"name": row[0], "place": row[1], "prise": row[2], "city": row[3], "system": row[4]}
        for row in result1
    ]
    with open("second_task_query1.json", "w", encoding="utf-8") as f:
        json.dump(query1_json, f, ensure_ascii=False, indent=4)

    query2 = """
    SELECT t.city, SUM(tr.prise) AS total_prise
    FROM tournament_results AS tr
    JOIN tournaments AS t ON tr.name = t.name
    GROUP BY t.city
    ORDER BY total_prise DESC
    """
    result2 = cursor.execute(query2).fetchall()
    print("Запрос 2: Общая сумма призовых по городам:")
    for row in result2:
        print(row)

    query2_json = [{"city": row[0], "total_prise": row[1]} for row in result2]
    with open("second_task_query2.json", "w", encoding="utf-8") as f:
        json.dump(query2_json, f, ensure_ascii=False, indent=4)

    query3 = """
    SELECT tr.name, tr.prise, t.city
    FROM tournament_results AS tr
    JOIN tournaments AS t ON tr.name = t.name
    WHERE tr.prise > 1000000
    ORDER BY tr.prise DESC
    """
    result3 = cursor.execute(query3).fetchall()
    print("Запрос 3: Турниры с призовыми выше 1 000 000:")
    for row in result3:
        print(row)

    query3_json = [
        {"name": row[0], "prise": row[1], "city": row[2]}
        for row in result3
    ]
    with open("second_task_query3.json", "w", encoding="utf-8") as f:
        json.dump(query3_json, f, ensure_ascii=False, indent=4)