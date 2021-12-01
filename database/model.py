import sqlite3

class Model:
    def __init__(self):
        self.db = sqlite3.connect("workmate.db")
        self.cur = self.db.cursor()

        self.create_tables()

        

    def create_tables(self):
        apps_table = """
            CREATE TABLE IF NOT EXISTS apps(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                path TEXT NOT NULL,
                index INT NOT NULL
            )
        """

        notes_table = """
            CREATE TABLE IF NOT EXISTS notes(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                body TEXT,
            )
        """

        todos_table = """
            CREATE TABLE IF NOT EXISTS todos(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                complete INT DEFAULT 0 NOT NULL,
                deadline NUMERIC
            )
        """
        self.cur.execute(apps_table)
        self.cur.execute(notes_table)
        self.cur.execute(todos_table)

    def save(self, table, data):
        # self.open_db()
        
        # data = [data] if type(data) != list else data
        # values = "(?, ?, ?)" if table == "notes" else "(?, ?, ?, ?)"

        # query = f"INSERT INTO {table} VALUES {values}"

        # self.cur.executemany(query, data)
        # self.db.commit()
        # self.db.close()
        print(data.keys())
        print(data.values())

    def read(self, table):

        query = f"SELECT * FROM {table}"
        
        self.cur.execute(query)
        data = self.cur.fetchall()
        self.db.close()

        return data

    def delete(self, table, name):
        query = f"DELETE FROM {table} WHERE name = (?)"
        self.cur.execute(query, (name,))
        self.db.commit()
        self.db.close()

    def update(self, table, name, data):
        self.open_db()

        query = f"DELETE FROM {table} WHERE name = (?)"

        self.cur.execute(query, (name,))
        self.db.commit()
        self.db.close()





    
    
        