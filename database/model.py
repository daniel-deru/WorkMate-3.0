import sqlite3
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from utils.globals import DB_PATH

class Model:
    def __init__(self):
        self.db = sqlite3.connect(DB_PATH)
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

        protected_apps_table = """
            CREATE TABLE IF NOT EXISTS protected_apps(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                path TEXT NOT NULL,
                sequence INTEGER NOT NULL,
                username TEXT,
                email TEXT,
                password TEXT NOT NULL
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

        settings_table = """
            CREATE TABLE IF NOT EXISTS settings(
                id TEXT DEFAULT 'settings' PRIMARY KEY,
                nightmode INTEGER DEFAULT 0,
                font TEXT DEFAULT 'Arial',
                color TEXT DEFAULT '#000000',
                vault_on INTEGER DEFAULT 1 NOT NULL,
                timer INTEGER DEFAULT 5 NOT NULL,
                calendar INTEGER DEFAULT 0 NOT NULL,
                twofa INTEGER DEFAULT 0 NOT NULL
            )
        """

        users_table = """
            CREATE TABLE IF NOT EXISTS user(
                id TEXT DEFAULT 'user' PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                password TEXT NOT NULL,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                twofa_key TEXT
            )
        """

        vault_table = """
            CREATE TABLE IF NOT EXISTS vault(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                data TEXT NOT NULL,
                key TEXT NOT NULL
            )
        """

        crypto_vault_table = """
            CREATE TABLE IF NOT EXISTS cryptovault(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                num_words INT NOT NULL,
                words TEXT NOT NULL,
                description TEXT NOT NULL,
                password TEXT NOT NULL
            )
        """

        app_vault_table = """
            CREATE TABLE IF NOT EXISTS appvault(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                sequence INT NOT NULL,
                path TEXT NOT NULL,
                username TEXT NOT NULL,
                email TEXT NOT NULL,
                password TEXT NOT NULL
            )
        """
        self.cur.execute(apps_table)
        self.cur.execute(notes_table)
        self.cur.execute(todos_table)
        self.cur.execute(settings_table)
        self.cur.execute(users_table)
        self.cur.execute(vault_table)
        self.cur.execute(protected_apps_table)
        self.cur.execute(crypto_vault_table)
        self.cur.execute(app_vault_table)

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
    
    def clearTable(self, table):
        query = f"""
            DROP TABLE IF EXISTS {table}
        """
        self.cur.execute(query)
        self.db.commit()
        self.db.close()
    
    def reset(self):
        query = """
            UPDATE settings SET nightmode = 0, font = 'Arial', color = '#000000' WHERE id = 'settings'
        """

        self.cur.execute(query)
        self.db.commit()
        self.db.close()
    
    def start(self):
        settings = Model().read("settings")
        if len(settings) == 0:
            data = {
                'nightmode': 0,
                'font': "Arial",
                'color': "#000000"
            }
            self.save('settings', data)

    def add_column(self, table_name, column_name, column_definition):
        query = f"ALTER TABLE {table_name} ADD {column_name} {column_definition}"
        self.cur.execute(query)

# model = Model()
# model.add_column("settings", "twofa", "INTEGER DEFAULT 0 NOT NULL")
# model.add_column("user", "twofa_key", "TEXT")









    
    
        