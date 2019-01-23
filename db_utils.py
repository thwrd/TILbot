import sqlite3

def get_database_connection(dbName):
    dbConnection = sqlite3.connect(dbName)
    return dbConnection

def create_facts_table(dbConnection):
    with dbConnection:
        cur = dbConnection.cursor()
        cur.execute('''CREATE TABLE facts 
                        (timeStamp BIGINT, postId TEXT, title TEXT,
                        permaLink TEXT, sourceUrl TEXT )''')
