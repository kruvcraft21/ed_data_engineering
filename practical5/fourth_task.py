from pymongo import MongoClient
import pandas as pd
import msgpack, json
from datetime import datetime
from mongo_utils import MongoEncoder

def parse_date(date):
    return datetime.strptime(date, "%Y-%m-%d")

def processing_item(item):
    item['registration_date'] = datetime.strptime(item["registration_date"], "%Y-%m-%d")
    item['_id'] = item.pop("user_id")
    return item

def dump2json(file_path, list_json):
    with open(file_path, "w") as file_to_json:
        json.dump(list_json, file_to_json, ensure_ascii=False, cls=MongoEncoder, indent=4)

with MongoClient("mongodb://192.168.122.186:27017/") as client:
    db = client["practical_five"]
    collection = db["fourth_task"]
    collection.drop()

    df = pd.read_csv("fourth_task/users.csv", converters={"registration_date":parse_date})
    df = df.rename(columns={"user_id": "_id"})
    collection.insert_many(df.to_dict("records"))

    with open("fourth_task/users.msgpack", "rb") as f:
        data = msgpack.load(f, object_hook=processing_item)

    collection.insert_many(data)

    print("\n1. Выборка:")
    print("Пользователи из East Craigport старше 30 лет")
    query_1 = {"city": "East Craigport", "age": {"$gt": 30}}
    result1_1 = collection.find(query_1).to_list()
    dump2json("fourth_task_result1_1.json", result1_1)
    print(result1_1)

    print("Пользователи, зарегистрированные в октябре 2022 года")
    query_2 = {"registration_date": {"$gte": datetime(2022, 10, 1), "$lt": datetime(2022, 11, 1)}}
    result1_2 = collection.find(query_2).to_list()
    dump2json("fourth_task_result1_2.json", result1_2)
    print(result1_2)

    print("Пользователи, чьи имена начинаются с 'J'")
    query_3 = {"name": {"$regex": "^J"}}
    result1_3 = collection.find(query_3).to_list()
    dump2json("fourth_task_result1_3.json", result1_3)
    print(result1_3)

    print("Пользователи с возрастом в диапазоне от 40 до 60 лет")
    query_4 = {"age": {"$gte": 40, "$lte": 60}}
    result1_4 = collection.find(query_4).to_list()
    dump2json("fourth_task_result1_4.json", result1_4)
    print(result1_4)

    print('Пользователи, не из города "East Craigport"')
    query_5 = {"city": {"$ne": "East Craigport"}}
    result1_5 = collection.find(query_5).to_list()
    dump2json("fourth_task_result1_5.json", result1_5)
    print(result1_5)

    print("\n2. Выборки с агрегацией:")
    print("Средний возраст пользователей по городам")
    pipeline_1 = [
        {"$group": {"_id": "$city", "average_age": {"$avg": "$age"}}},
        {"$sort": {"average_age": -1}}
    ]
    result2_1 = collection.aggregate(pipeline_1).to_list()
    dump2json("fourth_task_result2_1.json", result2_1)
    print(result2_1)

    print("Количество пользователей в каждом городе")
    pipeline_2 = [
        {"$group": {"_id": "$city", "user_count": {"$sum": 1}}},
        {"$sort": {"user_count": -1}}
    ]
    result2_2 = collection.aggregate(pipeline_2).to_list()
    dump2json("fourth_task_result2_2.json", result2_2)
    print(result2_2)

    print("Количество пользователей, зарегистрированных после 2022 года, по годам")
    pipeline_3 = [
        {"$match": {"registration_date": {"$gte": datetime(2022, 1, 1)}}},
        {"$project": {"year": {"$year": "$registration_date"}}},
        {"$group": {"_id": "$year", "user_count": {"$sum": 1}}}
    ]
    result2_3 = collection.aggregate(pipeline_3).to_list()
    dump2json("fourth_task_result2_3.json", result2_3)
    print(result2_3)

    print("Самый старший пользователь в каждом городе")
    pipeline_4 = [
        {"$sort": {"age": -1}},
        {"$group": {"_id": "$city", "oldest_user": {"$first": "$name"}, "age": {"$first": "$age"}}}
    ]
    result2_4 = collection.aggregate(pipeline_4).to_list()
    dump2json("fourth_task_result2_4.json", result2_4)
    print(result2_4)

    print("Число пользователей старше 40 по городам")
    result = collection.aggregate([{"$match": {"age": {"$gt": 40}}}, {"$group": {"_id": "$city", "count": {"$sum": 1}}}])
    dump2json("fourth_task_result2_5.json", result.to_list())
    print(result.to_list())

    # 3. Обновление/удаление данных
    print("\n3. Обновление/удаление данных:")
    print('Обновить город всех пользователей старше 60 лет на "GoldenTown"')
    update_1 = {"age": {"$gt": 60}}
    update_result_1 = collection.update_many(update_1, {"$set": {"city": "GoldenTown"}})
    print("Обновлено записей:", update_result_1.modified_count)

    print("Удалить всех пользователей младше 30 лет")
    delete_1 = {"age": {"$lt": 30}}
    delete_result_1 = collection.delete_many(delete_1)
    print("Удалено записей:", delete_result_1.deleted_count)

    print("Обновить возраст всех пользователей, добавив 1 год")
    update_2 = collection.update_many({}, {"$inc": {"age": 1}})
    print("Обновлено записей:", update_2.modified_count)

    print("Удалить пользователей, зарегистрированных до 2023 года")
    delete_2 = {"registration_date": {"$lt": datetime(2023, 1, 1)}}
    delete_result_2 = collection.delete_many(delete_2)
    print("Удалено записей:", delete_result_2.deleted_count)

    print('Обновить имя пользователя с ID 3 на "Tammy S."')
    update_3 = {"_id": 3}
    update_result_3 = collection.update_one(update_3, {"$set": {"name": "Tammy S."}})
    print("Обновлено записей:", update_result_3.modified_count)


