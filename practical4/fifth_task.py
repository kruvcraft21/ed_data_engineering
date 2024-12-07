from five_task.init_database import create_database
from five_task.load_data import load_data
from five_task.test_queries import execute_queries

# Название предметной области: Цифровой музыкальный магазин
#
# Описание предметной области:
# Модель данных представляет собой цифровой музыкальный магазин, который включает таблицы для управления
# информацией об исполнителях, альбомах, медиатреках.
# Медиа-данные были созданы на основе реальных данных из библиотеки iTunes, что
# позволяет получить разнообразную и реалистичную коллекцию музыкальных треков и альбомов.
#
# Файлы исходных данных находятся в папке five_task/data
#
# Скрипт инициализации базы данных: five_task/init_database.py
#
# Скрипт для загрузки данных из файлов в базу данных: five_task/load_data.py
#
# Файл базы данных: five_task/music_catalog.db
#
# Скрипт с выполнением запросов к базе данных: five_task/test_queries.py

create_database("five_task/music_catalog.db")
load_data('five_task/data/', "five_task/music_catalog.db")
execute_queries("five_task/queries_out/", "five_task/music_catalog.db")
