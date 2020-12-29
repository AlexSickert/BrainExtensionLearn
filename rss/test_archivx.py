

import sqlite3


def get_connect():
    db = sqlite3.connect('arxiv.db')
    return db


db = get_connect()

sql = """

select distinct date_str from articles order by date_str

"""

params = ()
cursor = db.cursor()
cursor.execute(sql, params)

res = cursor.fetchall()


for row in res:

    print("-------------------------")
    print (row)