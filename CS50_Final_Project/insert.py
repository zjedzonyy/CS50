import csv
import sqlite3

#read data from csv
with open('dane2.csv', 'r', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    data_to_insert = [(row['flavor'], row['description'], row['image'], row['price'], row['producer']) for row in reader]

#connect with db sqlite3
conn = sqlite3.connect('zayerbani2.db')
cursor = conn.cursor()

#insert data to table
cursor.executemany('''
INSERT INTO yerbas (flavor, description, image, price, producer) VALUES (?, ?, ?, ?, ?)
''', data_to_insert)

conn.commit()
conn.close()