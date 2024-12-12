import pickle
from mongo_utils import MongoEncoder, rename_key_nested
from pymongo import MongoClient

with MongoClient("mongodb://192.168.122.186:27017/") as client:
    db = client["practical_five"]
    collection = db["data"]

    with open("data/task_3_item.pkl", 'rb') as f:
        data = pickle.load(f)
    rename_key_nested(data, 'id', '_id')
    collection.insert_many(data)

    # 1. Удалить документы по предикату: salary < 25000 || salary > 175000
    print(f"Count documents in collection: {collection.count_documents({})}")
    collection.delete_many({"$or": [{"salary": {"$lt": 25000}}, {"salary": {"$gt": 175000}}]})
    print(f"Count documents in collection: {collection.count_documents({})}")

    # 2. Увеличить возраст (age) всех документов на 1
    query_avg_age_all = [{'$group': {'_id': None, "avg_age" : {"$avg" : "$age"}}}]
    print("Средний возраст", collection.aggregate(query_avg_age_all).to_list())
    collection.update_many({}, {"$inc": {"age": 1}})
    print("Средний возраст", collection.aggregate(query_avg_age_all).to_list())

    # 3. Поднять заработную плату на 5% для произвольно выбранных профессий
    selected_jobs = ["Бухгалтер", "Архитектор"]
    query_avg_salary_jobs = [
        {
            '$match': {'job': {"$in": selected_jobs}},
        },
        {
            '$group': {
                '_id': None,
                'avg_salary': {'$avg': '$salary'},
            }
        }
    ]
    print("Средняя зарплата", collection.aggregate(query_avg_salary_jobs).to_list())
    collection.update_many({"job": {"$in": selected_jobs}}, {"$mul": {"salary": 1.05}})
    print("Средняя зарплата", collection.aggregate(query_avg_salary_jobs).to_list())

    # 4. Поднять заработную плату на 7% для произвольно выбранных городов
    selected_cities = ["Хихон", "Вальядолид"]
    query_avg_city_jobs = [
        {
            '$match': {'city': {"$in": selected_cities}},
        },
        {
            '$group': {
                '_id': None,
                'avg_city': {'$avg': '$salary'},
            }
        }
    ]
    print("Средняя зарплата по городу", collection.aggregate(query_avg_city_jobs).to_list())
    collection.update_many({"city": {"$in": selected_cities}}, {"$mul": {"salary": 1.07}})
    print("Средняя зарплата по городу", collection.aggregate(query_avg_city_jobs).to_list())

    # 5. Поднять заработную плату на 10% для выборки по сложному предикату
    query_avg_complex_predicate = [
        {
            '$match': {
                "$and" : [
                    {'job': {"$in": selected_jobs}},
                    {'city': "Навалькарнеро"},
                    {'age' : {"$gte": 40, "$lte": 60}}

                ]
            },
        },
        {
            '$group': {
                '_id': None,
                'avg_city': {'$avg': '$salary'},
            }
        }
    ]
    complex_predicate = {
        "$and": [
            {"city": "Навалькарнеро"},
            {"job": {"$in": selected_jobs}},
            {"age": {"$gte": 40, "$lte": 60}}
        ]
    }
    print("Зарплата по сложному предикату", collection.aggregate(query_avg_complex_predicate).to_list())
    collection.update_many(complex_predicate, {"$mul": {"salary": 1.10}})
    print("Зарплата по сложному предикату", collection.aggregate(query_avg_complex_predicate).to_list())

    # 6. Удалить записи по произвольному предикату
    custom_predicate = {"year": {"$lt": 2010}}
    print(f"Count documents in collection: {collection.count_documents({})}")
    collection.delete_many(custom_predicate)
    print(f"Count documents in collection: {collection.count_documents({})}")



