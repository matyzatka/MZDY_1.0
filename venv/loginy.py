import sqlite3

with sqlite3.connect("databaze_loginy.db") as db:
    cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS databaze_loginy(
username VARCHAR,
password VARCHAR,
email VARCHAR);
""")

#cursor.execute("""DELETE FROM databaze_loginy WHERE username = ?""")

#db.commit()

cursor.execute("SELECT * FROM databaze_loginy")
print(cursor.fetchall())

db.commit()