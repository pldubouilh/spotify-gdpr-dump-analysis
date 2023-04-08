import pandas as pd
import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('mydatabase.db')

df = pd.read_sql_query(f"""
    SELECT count(*) as ttl, ip_addr_decrypted FROM mytable group by ip_addr_decrypted order by ttl desc
    limit 100
""", conn)

print(df.to_string())