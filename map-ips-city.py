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
lats = []
lons = []

# Loop through IPs and get lat/long
for ip in df['ip_addr_decrypted']:
    try:
        response = reader.city(ip)
        lat = response.location.latitude
        lon = response.location.longitude
        # normalise lat long
        lat = lat - (lat % 0.5)
        lon = lon - (lon % 0.5)
    except:
        lat = 0
        lon = 0

    lats.append(lat)
    lons.append(lon)

df['latitude'] = lats
df['longitude'] = lons
print("df", df)

# Remove countries with missing location information
df = df.dropna(subset=['latitude', 'longitude'])

# group identical lat long
df = df.groupby(['latitude', 'longitude']).sum().reset_index()

# find maximum
max_count = df['count'].max()

# # remove points with less than 5% of the maximum
# df = df[df['count'] > max_count * 0.0001]

# find large points
large_points = df[df['count'] > max_count * 0.10]
too_small_points = []

# regroup small points when they're within 0.5 of lat/long of a large point, add the count, and delete the small point
for i, row in df.iterrows():
    for j, rowlarge in large_points.iterrows():
        if abs(row['latitude'] - rowlarge['latitude']) < 1.5 and abs(row['longitude'] - rowlarge['longitude']) < 1.5:
            large_points.loc[j, 'count'] += row['count']
            too_small_points.append(i)

# remove satelites from df and merge large with df
df = df.drop(too_small_points)
df = pd.concat([df, large_points]).drop_duplicates(keep=False)

# Plot the map
fig = plt.figure(figsize=(10, 8))
m = Basemap(projection='merc', lat_0=0, lon_0=0, resolution='l', area_thresh=1000.0, llcrnrlon=-180, llcrnrlat=-80, urcrnrlon=180, urcrnrlat=80)
m.drawcoastlines()
m.fillcontinents(color='#cc9966')
m.drawcountries(linewidth=1.5, linestyle='solid', color='k', antialiased=1, ax=None, zorder=None)

# Draw the country boundaries and add annotations
for i, row in df.iterrows():
    lon, lat= m(row['longitude'], row['latitude'])
    marker_size = 20 + 50*(row['count'] / max_count)
    if row['count'] > 1000:
        label = str(int(row['count']/1000)) + "k"
    else:
        label = str(row['count'])
    plt.plot(lon, lat, 'ro', markersize=marker_size, alpha=0.6)
    plt.text(lon, lat, label, fontsize=10, ha='center', va='center', color='white', fontweight='bold')

plt.show()

# Close the database connection
conn.close()