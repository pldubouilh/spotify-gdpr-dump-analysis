from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import sqlite3
import pandas as pd
import geoip2.database

# Connect to the SQLite database
conn = sqlite3.connect('mydatabase.db')

YEAR = 2022

# Read the data
df = pd.read_sql_query(f"""
    SELECT ip_addr_decrypted, COUNT(*) AS count
    FROM mytable
    -- WHERE strftime('%Y', ts) AS year is "{YEAR}"
    GROUP BY ip_addr_decrypted
    ORDER BY count DESC
    """, conn)

# Initialize a reader for the GeoIP database
reader = geoip2.database.Reader('city.mmdb')

# Initialize lists to store the latitude and longitude values
city = []
country = []

# Loop through IPs and get lat/long
for ip in df['ip_addr_decrypted']:
    try:
        response = reader.city(ip)
        city.append(response.city.name)
        country.append(response.country.name)
    except:
        city.append("")
        country.append("")

df['city'] = city
df['country'] = country

# Remove countries with missing location information
df = df.dropna(subset=['city'])
df = df.dropna(subset=['country'])

# drop ip address
df = df.drop(columns=['ip_addr_decrypted'])

# group identical lat long
df = df.groupby(['city', 'country']).sum().reset_index()

# sort by count
df = df.sort_values(by=['count'], ascending=False)

# limit to top 20
df = df.head(20)

print("df", df.to_string())
