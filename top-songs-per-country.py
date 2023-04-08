import sqlite3
import pandas as pd

# Connect to the SQLite database
conn = sqlite3.connect('mydatabase.db')

# Define the SQL query
query = """
SELECT conn_country, master_metadata_track_name, master_metadata_album_artist_name, master_metadata_album_album_name, COUNT(*) as total_plays
FROM mytable
WHERE conn_country IN (SELECT DISTINCT conn_country FROM mytable)
GROUP BY conn_country, master_metadata_track_name, master_metadata_album_artist_name, master_metadata_album_album_name
HAVING COUNT(*) > 1
ORDER BY conn_country, total_plays DESC;
"""

# Execute the SQL query and retrieve the results as a pandas DataFrame
df = pd.read_sql_query(query, conn)

# Group the DataFrame by country and extract the top 10 songs for each country
grouped = df.groupby('conn_country')
top_songs = grouped.apply(lambda x: x.nlargest(10, 'total_plays'))
print("top_songs", top_songs.to_string())
