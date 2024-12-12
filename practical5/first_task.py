import pandas as pd
from pymongo import MongoClient
from mongo_utils import MongoEncoder
import json

with MongoClient("mongodb://192.168.122.186:27017/") as client:
    db = client["practical_five"]
    collection = db["data"]

    df = pd.read_csv("data/task_1_item.csv", sep=';')
    df = df.rename(columns={'id': '_id'})
    collection.insert_many(df.to_dict(orient='records'))

    # Запрос 1: Первые 10 записей, отсортированных по убыванию по полю salary
    query1 = collection.find().sort("salary", -1).limit(10).to_list()

    with open("first_task_query1.json", "w") as file:
        json.dump(query1, file, ensure_ascii=False, cls=MongoEncoder, indent=4)

    # Запрос 2: Первые 15 записей с age < 30, отсортированные по убыванию по полю salary
    query2 = collection.find({"$where": "this.age < 30"}).sort("salary", -1).limit(15).to_list()

    with open("first_task_query2.json", "w") as file:
        json.dump(query2, file, ensure_ascii=False, cls=MongoEncoder, indent=4)

    # Запрос 3: Первые 10 записей из города "Сеговия" и с профессиями "Менеджер", "IT-специалист", "Программист", отсортированные по возрасту
    city = "Сеговия"
    jobs = ["Менеджер", "IT-специалист", "Программист"]
    query3 = collection.find({"$where": f"this.city == '{city}' && {json.dumps(jobs)}.includes(this.job)"}).sort("age", 1).limit(10).to_list()

    with open("first_task_query3.json", "w") as file:
        json.dump(query3, file, ensure_ascii=False, cls=MongoEncoder, indent=4)

    # Запрос 4: Количество записей с фильтрацией
    age_range = {"$gte": 25, "$lte": 40}
    salary_condition = {"$or": [
        {"salary": {"$gt": 50000, "$lte": 75000}},
        {"salary": {"$gt": 125000, "$lt": 150000}}
    ]}
    query4 = collection.count_documents({
        "age": age_range,
        "year": {"$in": [2019, 2020, 2021, 2022]},
        "$and": [salary_condition]
    })

    print(query4)
    with open("first_task_query4.json", "w") as file:
        json.dump({"count":query4}, file, ensure_ascii=False, cls=MongoEncoder, indent=4)