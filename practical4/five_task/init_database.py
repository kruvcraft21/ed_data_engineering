import sqlite3

# Создание базы данных и таблиц
def create_database(path: str = "music_catalog.db"):
    with sqlite3.connect(path) as connection:
        cursor = connection.cursor()

        # SQL для создания таблиц
        cursor.execute("""
                CREATE TABLE IF NOT EXISTS Artist (
                    ArtistId INTEGER PRIMARY KEY,
                    Name TEXT NOT NULL
                );
            """)

        cursor.execute("""
                CREATE TABLE IF NOT EXISTS Album (
                    AlbumId INTEGER PRIMARY KEY,
                    Title TEXT NOT NULL,
                    ArtistId INTEGER NOT NULL,
                    FOREIGN KEY (ArtistId) REFERENCES Artist (ArtistId)
                );
            """)

        cursor.execute("""
                CREATE TABLE IF NOT EXISTS Genre (
                    GenreId INTEGER PRIMARY KEY,
                    Name TEXT NOT NULL
                );
            """)

        cursor.execute("""
                CREATE TABLE IF NOT EXISTS MediaType (
                    MediaTypeId INTEGER PRIMARY KEY,
                    Name TEXT NOT NULL
                );
            """)

        cursor.execute("""
                CREATE TABLE IF NOT EXISTS Playlist (
                    PlaylistId INTEGER PRIMARY KEY,
                    Name TEXT NOT NULL
                );
            """)

        cursor.execute("""
                CREATE TABLE IF NOT EXISTS Track (
                    TrackId INTEGER PRIMARY KEY,
                    Name TEXT NOT NULL,
                    AlbumId INTEGER,
                    MediaTypeId INTEGER,
                    GenreId INTEGER,
                    Composer TEXT,
                    Milliseconds INTEGER NOT NULL,
                    Bytes INTEGER,
                    UnitPrice REAL NOT NULL,
                    FOREIGN KEY (AlbumId) REFERENCES Album (AlbumId),
                    FOREIGN KEY (MediaTypeId) REFERENCES MediaType (MediaTypeId),
                    FOREIGN KEY (GenreId) REFERENCES Genre (GenreId)
                );
            """)

        cursor.execute("""
                CREATE TABLE IF NOT EXISTS PlaylistTrack (
                    PlaylistId INTEGER,
                    TrackId INTEGER,
                    PRIMARY KEY (PlaylistId, TrackId),
                    FOREIGN KEY (PlaylistId) REFERENCES Playlist (PlaylistId),
                    FOREIGN KEY (TrackId) REFERENCES Track (TrackId)
                );
            """)

        connection.commit()
    print("База данных и таблицы успешно созданы.")

# Вызов функции для создания базы данных
if __name__ == "__main__":
    create_database()
