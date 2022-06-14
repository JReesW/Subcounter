import sqlite3
import random


con = sqlite3.connect("database.db")
cur = con.cursor()


cur.execute("DROP TABLE IF EXISTS records")

cur.execute("""
    CREATE TABLE records (year int, month int, day int, subs int)
""")


days = [
    (1, 3714),
    (3, 3742),
    (4, 3744),
    (5, 3751),
    (8, 3760),
    (9, 3780),
    (10, 3792),
    (11, 3801),
    (13, 3810)
]
for day, s in days:
    cur.execute(f"INSERT INTO records VALUES (2022, 6, {day}, {s})")
    con.commit()
