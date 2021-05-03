import sqlite3
from textwrap import dedent

class sqlite3_database(object):

    def __init__(self, database='database.db'):
        self.database = database
        self.connection = None
        self.cursor = None
        self.connected = False
        self.connect()
        self.close()

    def connect(self):
        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()
        self.connected = True

    def close(self):
        self.connection.commit()
        self.connection.close()
        self.connected = False

    def insert_result(self, time_stamp, subreddit, post_title, link):
        self.connect()
        self.cursor.execute('INSERT INTO results VALUES (?,?,?,?,?)',
                            (None, time_stamp, subreddit, post_title, link))
        self.close()

    def create_database(self):
        self.connect()
        self.cursor.execute(dedent('''CREATE TABLE if not exists results (
        id integer not null primary key,
        date_time text,
        subreddit text,
        post_title text,
        post_url text)'''))
        self.close()

    def query_last_record(self):
        self.connect()
        self.cursor.execute(dedent("""select * from results 
        where id = (select max(id) from results);"""))
        return self.cursor.fetchall()
