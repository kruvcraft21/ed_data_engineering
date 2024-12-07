import sqlite3
import json
import pandas as pd

# Загрузка данных в базу
def load_data(path_data: str = 'data/', path_db: str = "music_catalog.db"):
    with sqlite3.connect(path_db) as connection:
        cursor = connection.cursor()

        # Загрузка Artist
        with open(path_data + "Artist.json", "r") as f:
            artists = json.load(f)
            cursor.executemany(
                "INSERT OR IGNORE INTO Artist (ArtistId, Name) VALUES (?, ?)",
                [(a["ArtistId"], a["Name"]) for a in artists]
            )

        # Загрузка Album
        with open(path_data + "Album.json", "r") as f:
            albums = json.load(f)
            cursor.executemany(
                "INSERT OR IGNORE INTO Album (AlbumId, Title, ArtistId) VALUES (?, ?, ?)",
                [(a["AlbumId"], a["Title"], a["ArtistId"]) for a in albums]
            )

        # Загрузка Genre
        with open(path_data + "Genre.json", "r") as f:
            genres = json.load(f)
            cursor.executemany(
                "INSERT OR IGNORE INTO Genre (GenreId, Name) VALUES (?, ?)",
                [(g["GenreId"], g["Name"]) for g in genres]
            )

        # Загрузка MediaType
        with open(path_data + "MediaType.json", "r") as f:
            media_types = json.load(f)
            cursor.executemany(
                "INSERT OR IGNORE INTO MediaType (MediaTypeId, Name) VALUES (?, ?)",
                [(m["MediaTypeId"], m["Name"]) for m in media_types]
            )

        # Загрузка Playlist
        with open(path_data + "Playlist.json", "r") as f:
            playlists = json.load(f)
            cursor.executemany(
                "INSERT OR IGNORE INTO Playlist (PlaylistId, Name) VALUES (?, ?)",
                [(p["PlaylistId"], p["Name"]) for p in playlists]
            )

        # Загрузка Track
        pd.read_csv(path_data + "Track.csv").to_sql("Track", connection, if_exists="replace", index=False)

        # Загрузка PlaylistTrack
        with open(path_data + "PlaylistTrack.json", "r") as f:
            playlist_tracks = json.load(f)
            cursor.executemany(
                "INSERT OR IGNORE INTO PlaylistTrack (PlaylistId, TrackId) VALUES (?, ?)",
                [(pt["PlaylistId"], pt["TrackId"]) for pt in playlist_tracks]
            )

        connection.commit()

if __name__ == "__main__":
    load_data()
