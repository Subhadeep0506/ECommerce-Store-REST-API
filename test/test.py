import sqlite3

connection = sqlite3.connect('./test/data.db')

cursor = connection.cursor()

create_table = "CREATE TABLE IF NOT EXISTS users (id int PRIMARY KEY, username text, password text)"
cursor.execute(create_table)

user1 = (1, "bob", "1234")

insert_query = "INSERT INTO users VALUES (?, ?, ?)"

cursor.execute(insert_query, user1)

users = [
  (2, "rolf", "2345"),
  (3, "smith", "3456"),
  (4, "john", "4567"),
  (5, "clint", "5678")
]

cursor.executemany(insert_query, users)

select_query = "SELECT username, password FROM users"
for row in cursor.execute(select_query):
  print(row)

# commiting the changes to database
connection.commit()
# closing the connection to database
connection.close()