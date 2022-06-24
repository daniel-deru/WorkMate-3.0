import sqlite3
import os
import sys
from cryptography.fernet import Fernet

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from utils.globals import DB_PATH
from utils.encryption import Encryption

encryption = Encryption()

class Model:
    def __init__(self):
        self.db = sqlite3.connect(f"{DB_PATH}test.db")
        self.cur = self.db.cursor()
        self.create_table_names()
        self.create_tables()
        self.fill_defaults()
        

    def create_tables(self):
        # enc = encryption.encrypt
        enc = lambda s: s
        apps_table_def = {
            "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
            "name": "TEXT NOT NULL",
            "path": "TEXT NOT NULL",
            "sequence": "INTEGER NOT NULL"
        }
        
        notes_table_def = {
            "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
            "name": "TEXT NOT NULL",
            "body": "TEXT"
        }
        
        todos_table_def = {
            "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
            "name": "TEXT NOT NULL",
            "complete": f"TEXT DEFAULT '{enc('0')}' NOT NULL",
            "deadline": "TEXT"
        }
        
        settings_table_def = {
            "id": f"TEXT DEFAULT '{enc('settings')}' PRIMARY KEY",
            "nightmode": f"TEXT DEFAULT '{enc('0')}'",
            "font": f"TEXT DEFAULT '{enc('Arial')}'",
            "color": f"TEXT DEFAULT '{enc('#000000')}'",
            "vault_on": f"TEXT DEFAULT '{enc('0')}' NOT NULL",
            "timer": f"TEXT DEFAULT '{enc('5')}' NOT NULL",
            "calendar": f"TEXT DEFAULT '{enc('0')}' NOT NULL",
            "twofa": f"TEXT DEFAULT '{enc('0')}' NOT NULL"
        }
        
        users_table_def = {
            "id": f"TEXT DEFAULT '{enc('user')}' PRIMARY KEY",
            "name": "TEXT NOT NULL",
            "email": "TEXT NOT NULL",
            "password": "TEXT NOT NULL",
            "question": "TEXT NOT NULL",
            "answer": "TEXT NOT NULL",
            "twofa_key": "TEXT"
        }
        
        vault_table_def = {
            "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
            "type": "TEXT NOT NULL",
            "name": "TEXT NOT NULL",
            "data": "TEXT NOT NULL"
        }
        
        
        
        self.create_table("apps", apps_table_def)
        self.create_table("notes", notes_table_def)
        self.create_table("todos", todos_table_def)
        self.create_table("settings", settings_table_def)
        self.create_table("user", users_table_def)
        self.create_table("vault", vault_table_def)
        
    def create_table(self, tablename: str, fields: object):
        encrypted_table_name = encryption.encrypt(tablename)
        
        new_table = self.insert_table_name(encrypted_table_name)
        
        names = list(fields.keys())
        definitions = list(fields.values())
        
        table_definition = ""
        
        for i in range(len(names)):
            encrypted_name = encryption.encrypt(names[i])
            table_definition += f"[{encrypted_name}] {definitions[i]}"
            if i < len(names) - 1: table_definition += ",\n\t\t"

        table_query = f"""
            CREATE TABLE IF NOT EXISTS [{encrypted_table_name}](
                {table_definition}
            )
        """
        if new_table: self.cur.execute(table_query)

    def save(self, table, data):
        keys = f'{", ".join(data.keys())}'
        values = ", ".join(list(map(lambda v: "?", data.keys())))
        
        

        query = f"INSERT INTO {table}({keys}) VALUES ({values})"

        self.cur.executemany(query, [tuple(data.values())])
        self.db.commit()
        self.db.close()
        
        

    def read(self, table):
        if table != "tablenames":
            table = self.get_encrypted_table_name(table)
            
        query = f"SELECT * FROM [{table}]"
        meta = self.cur.execute(query)
        data = self.cur.fetchall()
        for desc in list(meta.description):
            print(encryption.decrypt(desc[0]))
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
    
    def drop_table(self, table):
        self.cur.execute(f"DROP TABLE {table}")
        
    def create_table_names(self):
        query = """CREATE TABLE IF NOT EXISTS tablenames(
                name TEXT NOT NULL
            )"""
        self.cur.execute(query)
        
    def insert_table_name(self, value: str):
        get_query = "SELECT * FROM tablenames"
        self.cur.execute(get_query)
        tables = self.cur.fetchall()
        
        for table in tables:
            existing_decrypted_table = encryption.decrypt(table[0])
            decrypted_table = encryption.decrypt(value)
            if existing_decrypted_table == decrypted_table:
                return False
        
        query = "INSERT INTO tablenames (name) VALUES (?)"
        self.cur.execute(query, (value,))
        self.db.commit()
        return True

    def get_encrypted_table_name(self, tablename):
        self.cur.execute("SELECT * FROM tablenames")
        tables = self.cur.fetchall()
        
        for table in tables:
            decrypted_table = encryption.decrypt(table[0])
            if tablename == decrypted_table:
                return table[0]
            
        return None
    
    # get a dict of the table names that map to the encrypted table names
    def get_encrypted_table_cols(self, table: str) -> object:
        decrypted_table = self.get_encrypted_table_name(table)
        
        query = f"SELECT * FROM [{decrypted_table}]"
        data = self.cur.execute(query)
        table_columns = {}
        
        for meta in data.description:
            name = encryption.decrypt(meta[0])
            table_columns[name] = meta[0]
            
        return table_columns
        
    
    def fill_defaults(self):
        enc = encryption.encrypt
        settings = self.get_encrypted_table_name("settings")
        
        get_query = f"SELECT * FROM [{settings}]"
        self.cur.execute(get_query)
        settings_data = self.cur.fetchall()
        
        if len(settings_data) < 1:
            query = f"INSERT INTO [{settings}] VALUES ('{enc('settings')}', '{enc('0')}', '{enc('Arial')}', '{enc('#000000')}', '{enc('0')}', '{enc('5')}', '{enc('0')}', '{enc('0')}')"
            print(query)
            self.cur.execute(query)
            self.db.commit()
        
model = Model()
settings = model.read("settings")
# print(settings)