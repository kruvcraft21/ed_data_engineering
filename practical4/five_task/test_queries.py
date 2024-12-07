import sqlite3
import json

def get_dict_from_exec(cursor):
    return [dict(zip([desc[0] for desc in cursor.description], row)) for row in cursor.fetchall()]

# Функция для выполнения запросов
def execute_queries(path_out: str = 'queries_out/', path_db: str = "music_catalog.db"):
    with sqlite3.connect(path_db) as connection:
        cursor = connection.cursor()

        # Запрос 1: Выборка с простым условием + сортировка + ограничение количества
        cursor.execute("""
                SELECT Name, Milliseconds
                FROM Track
                WHERE Milliseconds > 300000
                ORDER BY Milliseconds DESC
                LIMIT 5;
            """)
        result1 = get_dict_from_exec(cursor)
        with open(path_out + "query_1.json", "w") as f:
            json.dump(result1, f, ensure_ascii=False, indent=4)

        # Запрос 2: Подсчёт треков по жанрам
        cursor.execute("""
                SELECT Genre.Name, COUNT(Track.TrackId) AS TrackCount
                FROM Genre
                JOIN Track ON Genre.GenreId = Track.GenreId
                GROUP BY Genre.Name;
            """)
        result2 = get_dict_from_exec(cursor)
        with open(path_out + "query_2.json", "w") as f:
            json.dump(result2, f, ensure_ascii=False, indent=4)

        # Запрос 3: Группировка альбомов по артистам
        cursor.execute("""
                SELECT Artist.Name, COUNT(Album.AlbumId) AS AlbumCount
                FROM Artist
                JOIN Album ON Artist.ArtistId = Album.ArtistId
                GROUP BY Artist.Name;
            """)
        result3 = get_dict_from_exec(cursor)
        with open(path_out + "query_3.json", "w") as f:
            json.dump(result3, f, ensure_ascii=False, indent=4)

        # Запрос 4: Суммарное время треков в каждом плейлисте
        cursor.execute("""
                SELECT Playlist.Name, SUM(Track.Milliseconds) AS TotalMilliseconds
                FROM Playlist
                JOIN PlaylistTrack ON Playlist.PlaylistId = PlaylistTrack.PlaylistId
                JOIN Track ON PlaylistTrack.TrackId = Track.TrackId
                GROUP BY Playlist.Name;
            """)
        result4 = get_dict_from_exec(cursor)
        with open(path_out + "query_4.json", "w") as f:
            json.dump(result4, f, ensure_ascii=False, indent=4)

        # Запрос 5: Обновление цены треков по жанру
        cursor.execute("""
                UPDATE Track
                SET UnitPrice = UnitPrice * 1.1
                WHERE GenreId = 1;
            """)
        connection.commit()
        with open(path_out + "query_5.json", "w") as f:
            json.dump({"message": "Цены треков в жанре 'Rock' увеличены на 10%"}, f, ensure_ascii=False, indent=4)

        # Запрос 6: Выборка топ-3 самых дорогих треков
        cursor.execute("""
                SELECT Name, UnitPrice
                FROM Track
                ORDER BY UnitPrice DESC
                LIMIT 3;
            """)
        result6 = get_dict_from_exec(cursor)
        with open(path_out + "query_6.json", "w") as f:
            json.dump(result6, f, ensure_ascii=False, indent=4)

        # Запрос 7: Подсчёт общего количества треков и альбомов
        cursor.execute("""
                SELECT 
                    (SELECT COUNT(*) FROM Track) AS TotalTracks,
                    (SELECT COUNT(*) FROM Album) AS TotalAlbums;
            """)
        result7 = cursor.fetchone()
        with open(path_out + "query_7.json", "w") as f:
            json.dump({"TotalTracks": result7[0], "TotalAlbums": result7[1]}, f, ensure_ascii=False, indent=4)

# Выполнение запросов
if __name__ == "__main__":
    execute_queries()
