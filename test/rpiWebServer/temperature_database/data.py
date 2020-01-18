import sqlite3 as lite
import sys

con =lite.connect('tempdata.db')

with con:
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS TMP_data")
    cur.execute("CREATE TABLE TMP_data (timestamp DATATIME, temp NUMERIC)")