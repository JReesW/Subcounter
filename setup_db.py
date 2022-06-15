import sqlite3
import random


con = sqlite3.connect("database.db")
cur = con.cursor()


cur.execute("DROP TABLE IF EXISTS records")

cur.execute("""
    CREATE TABLE minecraft_survival (year int, month int, day int, subs int)
""")

cur.execute("""
    CREATE TABLE mc_survival (year int, month int, day int, subs int)
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

days2 = [
    (1, 1327),
    (3, 1327),
    (4, 1327),
    (5, 1327),
    (8, 1327),
    (9, 1327),
    (10, 1327),
    (11, 1327),
    (13, 1327),
    (14, 1328)
]

for day, s in days:
    cur.execute(f"INSERT INTO minecraft_survival VALUES (2022, 6, {day}, {s})")
    con.commit()

for day, s in days2:
    cur.execute(f"INSERT INTO mc_survival VALUES (2022, 6, {day}, {s})")
    con.commit()
