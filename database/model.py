import sqlite3

class Model:
    def __init__(self):
        self.db = sqlite3.connect("./database/workmate.db")
        self.cur = self.db.cursor()

        self.create_tables()

    def create_tables(self):
        apps_table = """
            CREATE TABLE IF NOT EXISTS apps(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                path TEXT NOT NULL,
                sequence INTEGER NOT NULL
            )
        """

        notes_table = """
            CREATE TABLE IF NOT EXISTS notes(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                body TEXT
            )
        """

        todos_table = """
            CREATE TABLE IF NOT EXISTS todos(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                complete INTEGER DEFAULT 0 NOT NULL,
                deadline TEXT
            )
        """
        self.cur.execute(apps_table)
        self.cur.execute(notes_table)
        self.cur.execute(todos_table)

    def save(self, table, data): 
        keys = f'{", ".join(data.keys())}'
        values = ", ".join(list(map(lambda v: "?", data.keys())))

        query = f"INSERT INTO {table}({keys}) VALUES ({values})"

        self.cur.executemany(query, [tuple(data.values())])
        self.db.commit()
        self.db.close()
        
        

    def read(self, table):

        query = f"SELECT * FROM {table}"
        
        self.cur.execute(query)
        data = self.cur.fetchall()
        self.db.close()

        return data

    def delete(self, table, id):
        query = f"DELETE FROM {table} WHERE id = (?)"
        self.cur.execute(query, (id,))
        self.db.commit()
        self.db.close()

    def update(self, table, data, id):
        fields = data.keys()
        values = list(data.values())
        values.append(id)
        data_string = ", ".join(list(map(lambda a: f"{a} = ?", fields)))
        

 
        query = f"UPDATE {table} SET {data_string} WHERE id = ?"

        self.cur.execute(query, values)
        self.db.commit()
        self.db.close()








    
    
        