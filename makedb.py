import sys
import json
import os
import sqlite3

#  read data path from first argument
if len(sys.argv) != 2 or sys.argv[1] in ["-h", "--help"]:
    print("""Usage: python makedb.py [path_to_json_folder]""")
    sys.exit(0)

path_to_json_folder = sys.argv[1]

# Connect to the SQLite database
conn = sqlite3.connect('mydatabase.db')

print("scanning", path_to_json_folder)

# Create a table to store the JSON data
conn.execute('''
    CREATE TABLE IF NOT EXISTS mytable (
        ts TEXT,
        username TEXT,
        platform TEXT,
        ms_played INTEGER,
        conn_country TEXT,
        ip_addr_decrypted TEXT,
        user_agent_decrypted TEXT,
        master_metadata_track_name TEXT,
        master_metadata_album_artist_name TEXT,
        master_metadata_album_album_name TEXT,
        spotify_track_uri TEXT,
        episode_name TEXT,
        episode_show_name TEXT,
        spotify_episode_uri TEXT,
        reason_start TEXT,
        reason_end TEXT,
        shuffle BOOLEAN,
        skipped TEXT,
        offline BOOLEAN,
        offline_timestamp INTEGER,
        incognito_mode BOOLEAN
    )
''')

# Loop through each JSON file in the directory
for filename in os.listdir(path_to_json_folder):
    if filename.endswith('.json'):
        # Read the JSON data from the file
        with open(os.path.join(path_to_json_folder, filename)) as json_file:
            json_data = json.load(json_file)

        # Insert each record from the JSON array into the database
        for record in json_data:
            conn.execute('''
                INSERT INTO mytable (
                    ts,
                    username,
                    platform,
                    ms_played,
                    conn_country,
                    ip_addr_decrypted,
                    user_agent_decrypted,
                    master_metadata_track_name,
                    master_metadata_album_artist_name,
                    master_metadata_album_album_name,
                    spotify_track_uri,
                    episode_name,
                    episode_show_name,
                    spotify_episode_uri,
                    reason_start,
                    reason_end,
                    shuffle,
                    skipped,
                    offline,
                    offline_timestamp,
                    incognito_mode
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                record['ts'],
                record['username'],
                record['platform'],
                record['ms_played'],
                record['conn_country'],
                record['ip_addr_decrypted'],
                record['user_agent_decrypted'],
                record['master_metadata_track_name'],
                record['master_metadata_album_artist_name'],
                record['master_metadata_album_album_name'],
                record['spotify_track_uri'],
                record['episode_name'],
                record['episode_show_name'],
                record['spotify_episode_uri'],
                record['reason_start'],
                record['reason_end'],
                record['shuffle'],
                record['skipped'],
                record['offline'],
                record['offline_timestamp'],
                record['incognito_mode']
            ))

# Commit the changes and close the database connection
conn.commit()
conn.close()
