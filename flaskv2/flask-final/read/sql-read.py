#!/usr/bin/python3
import sqlite3
import time
def getSingleRows():
    
    connection = sqlite3.connect('/DataVolume/Database.db')
    cursor = connection.cursor()
    print("Connected to database")

    sqlite_select_query = """SELECT * from dht"""
    cursor.execute(sqlite_select_query)
    print("Fetching single row")
    while True:    
        try:
            record = cursor.fetchone()
            print(record)
            time.sleep(1)
        except sqlite3.Error as error:
            print("Failed to read data from table", error)
    cursor.close()
    connection.close()
    print("The Sqlite connection is closed")

getSingleRows()
