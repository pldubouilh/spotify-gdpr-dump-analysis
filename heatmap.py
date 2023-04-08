import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

# Connect to database
conn = sqlite3.connect('mydatabase.db')
c = conn.cursor()

# Retrieve data
c.execute("""
    SELECT strftime('%j', ts) - 1 as day, strftime('%W', ts) as week, SUM(ms_played) as total_ms_played
    FROM mytable
    WHERE strftime('%Y', ts) == "2022"
    GROUP BY day, week
""")
data = c.fetchall()
# print("data", data)

# Compute maximum value for normalization
max_value = max([d[2] for d in data])

# Create matrix for heatmap
matrix = np.zeros((53, 365))
for d in data:
    print("d", d)
    matrix[int(d[1]), int(d[0])] = d[2]

# Create heatmap
fig, ax = plt.subplots(figsize=(12, 6))
im = ax.imshow(matrix, cmap='YlOrRd')

# Set tick labels
week_labels = ['Week ' + str(i) for i in range(1, 54)]
day_labels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
ax.set_xticks(np.arange(0, 365, 7))
ax.set_xticklabels(week_labels)
ax.set_yticks(np.arange(0, 7))
ax.set_yticklabels(day_labels)

# Set colorbar
cbar = ax.figure.colorbar(im, ax=ax)
cbar.ax.set_ylabel('Total ms played', rotation=-90, va="bottom")

# Set title and show plot
ax.set_title('Total ms played by week and day of the year')
fig.tight_layout()
plt.show()