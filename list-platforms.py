import pandas as pd
import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('mydatabase.db')


# Query the top 100 most listened to songs per year
df = pd.read_sql_query(f"""
    SELECT count(*) as ttl, platform FROM mytable group by platform order by ttl desc
""", conn)

# Print the top 100 most listened to songs per year
print(df.to_string())