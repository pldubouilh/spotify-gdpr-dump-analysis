import pandas as pd
import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('mydatabase.db')

YEAR = 2022

# Query the top 100 most listened to songs per year
df = pd.read_sql_query(f"""
    SELECT
        master_metadata_track_name,
        master_metadata_album_artist_name,
        master_metadata_album_album_name,
        COUNT(*) AS play_count
    FROM mytable
    WHERE master_metadata_track_name IS NOT NULL
    -- and strftime('%Y', ts) == "{YEAR}"
    GROUP BY
    -- year,
        master_metadata_track_name,
        master_metadata_album_artist_name,
        master_metadata_album_album_name
    ORDER BY play_count DESC
    LIMIT 100
""", conn)

# Print the top 100 most listened to songs per year
print(df.to_string())