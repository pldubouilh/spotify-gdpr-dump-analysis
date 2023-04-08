import sqlite3
from collections import Counter

# connect to the database
conn = sqlite3.connect('mydatabase.db')
cursor = conn.cursor()

# execute the SQL query and retrieve the results as a list of tuples
query = '''
    SELECT master_metadata_track_name
    FROM mytable
    GROUP BY master_metadata_track_name
'''
results = cursor.execute(query).fetchall()

# flatten the list of tuples into a list of song titles
song_titles = [title for (title,) in results]

# count the occurrences of each word in the song titles using Counter
word_counts = Counter()
for title in song_titles:
    if title is None:
        continue
    words = title.split()
    word_counts.update(words)

# print the 10 most common words
for word, count in word_counts.most_common(300):
    print(word, count)