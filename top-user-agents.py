import pandas as pd
import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('mydatabase.db')

df = pd.read_sql_query(f"""
    SELECT count(*) as ttl, user_agent_decrypted FROM mytable group by user_agent_decrypted order by ttl desc
""", conn)

print(df.to_string())