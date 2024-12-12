import json
import msgpack
from pymongo import MongoClient
from mongo_utils import MongoEncoder, rename_key_nested

with MongoClient("mongodb://192.168.122.186:27017/") as client:
    db = client["practical_five"]
    collection = db["data"]

    with open("data/task_2_item.msgpack", 'rb') as f:
        data = msgpack.load(f)

    rename_key_nested(data, "id", "_id")
    collection.insert_many(data)

    # 1. минимальной, средней, максимальной salary
    pipeline_salary_stats = [
        {
            "$group": {
                "_id": None,
                "min_salary": {"$min": "$salary"},
                "avg_salary": {"$avg": "$salary"},
                "max_salary": {"$max": "$salary"}
            }
        }
    ]
    query1 = collection.aggregate(pipeline_salary_stats).to_list()
    print("query1: ", query1)
    with open("second_task_query1.json", 'w') as f:
        json.dump(query1, f, ensure_ascii=False, cls=MongoEncoder, indent=4)

    # 2. количества данных по представленным профессиям
    pipeline_profession_count = [
        {
            "$group": {
                "_id": "$job",
                "count": {"$sum": 1}
            }
        }
    ]
    query2 = collection.aggregate(pipeline_profession_count).to_list()
    print("query2: ", query2)
    with open("second_task_query2.json", 'w') as f:
        json.dump(query2, f, ensure_ascii=False, cls=MongoEncoder, indent=4)

    # 3. минимальной, средней, максимальной salary по городу
    pipeline_salary_by_city = [
        {
            "$group": {
                "_id": "$city",
                "min_salary": {"$min": "$salary"},
                "avg_salary": {"$avg": "$salary"},
                "max_salary": {"$max": "$salary"}
            }
        }
    ]
    query3 = collection.aggregate(pipeline_salary_by_city).to_list()
    print("query3: ", query3)
    with open("second_task_query3.json", 'w') as f:
        json.dump(query3, f, ensure_ascii=False, cls=MongoEncoder, indent=4)

    # 4. минимальной, средней, максимальной salary по профессии
    pipeline_salary_by_job = [
        {
            "$group": {
                "_id": "$job",
                "min_salary": {"$min": "$salary"},
                "avg_salary": {"$avg": "$salary"},
                "max_salary": {"$max": "$salary"}
            }
        }
    ]
    query4 = collection.aggregate(pipeline_salary_by_job).to_list()
    print("query4: ", query4)
    with open("second_task_query4.json", 'w') as f:
        json.dump(query4, f, ensure_ascii=False, cls=MongoEncoder, indent=4)

    # 5. минимального, среднего, максимального возраста по городу
    pipeline_age_by_city = [
        {
            "$group": {
                "_id": "$city",
                "min_age": {"$min": "$age"},
                "avg_age": {"$avg": "$age"},
                "max_age": {"$max": "$age"}
            }
        }
    ]
    query5 = collection.aggregate(pipeline_age_by_city).to_list()
    print("query5: ", query5)
    with open("second_task_query5.json", 'w') as f:
        json.dump(query5, f, ensure_ascii=False, cls=MongoEncoder, indent=4)

    # 6. минимального, среднего, максимального возраста по профессии
    pipeline_age_by_job = [
        {
            "$group": {
                "_id": "$job",
                "min_age": {"$min": "$age"},
                "avg_age": {"$avg": "$age"},
                "max_age": {"$max": "$age"}
            }
        }
    ]
    query6 = collection.aggregate(pipeline_age_by_job).to_list()
    print("query6: ", query6)
    with open("second_task_query6.json", 'w') as f:
        json.dump(query6, f, ensure_ascii=False, cls=MongoEncoder, indent=4)

    # 7. максимальной заработной платы при минимальном возрасте
    pipeline_max_salary_min_age = [
        {
            "$sort": {"age": 1, "salary": -1}
        },
        {
            "$limit": 1
        }
    ]
    query7 = collection.aggregate(pipeline_max_salary_min_age).to_list()
    print("query7: ", query7)
    with open("second_task_query7.json", 'w') as f:
        json.dump(query7, f, ensure_ascii=False, cls=MongoEncoder, indent=4)

    # 8. минимальной заработной платы при максимальной возрасте
    pipeline_min_salary_max_age = [
        {
            "$sort": {"age": -1, "salary": 1}
        },
        {
            "$limit": 1
        }
    ]
    query8 = collection.aggregate(pipeline_min_salary_max_age).to_list()
    print("query8: ", query8)
    with open("second_task_query8.json", 'w') as f:
        json.dump(query8, f, ensure_ascii=False, cls=MongoEncoder, indent=4)

    # 9. минимального, среднего, максимального возраста по городу, при условии,
    # что заработная плата больше 50000, отсортировать вывод по убыванию по полю avg
    pipeline_age_salary_filtered = [
        {
            "$match": {"salary": {"$gt": 50000}}
        },
        {
            "$group": {
                "_id": "$city",
                "min_age": {"$min": "$age"},
                "avg_age": {"$avg": "$age"},
                "max_age": {"$max": "$age"}
            }
        },
        {
            "$sort": {"avg_age": -1}
        }
    ]
    query9 = collection.aggregate(pipeline_age_salary_filtered).to_list()
    print("query9: ", query9)
    with open("second_task_query9.json", 'w') as f:
        json.dump(query9, f, ensure_ascii=False, cls=MongoEncoder, indent=4)

    # 10. вывод минимальной, средней, максимальной salary в произвольно заданных
    # диапазонах по городу, профессии, и возрасту: 18<age<25 & 50<age<65
    pipeline_salary_age_ranges_50_65 = [
        {
            "$match":{
                    "$or": [
                    {"age": {"$gte": 18, "$lt": 25}},
                    {"age": {"$gte": 50, "$lt": 65}}
            ]},
        },
        {
            "$group": {
                "_id": {"city": "$city", "job": "$job"},
                "min_salary": {"$min": "$salary"},
                "avg_salary": {"$avg": "$salary"},
                "max_salary": {"$max": "$salary"}
            }
        }
    ]
    query10 = collection.aggregate(pipeline_salary_age_ranges_50_65).to_list()
    print("query10: ", query10)
    with open("second_task_query10.json", 'w') as f:
        json.dump(query10, f, ensure_ascii=False, cls=MongoEncoder, indent=4)

    # 11. Custom
    pipeline_custom_query = [
        {
            "$match": {"city": "Семана", "salary": {"$gt": 100000}}
        },
        {
            "$group": {
                "_id": "$job",
                "total_salary": {"$sum": "$salary"},
                "avg_salary": {"$avg": "$salary"}
            }
        },
        {
            "$sort": {"avg_salary": -1}
        }
    ]
    query11 = collection.aggregate(pipeline_custom_query).to_list()
    print("query11: ", query11)
    with open("second_task_query11.json", 'w') as f:
        json.dump(query11, f, ensure_ascii=False, cls=MongoEncoder, indent=4)