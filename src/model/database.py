import sqlite3

class Database:
    def __init__(self, db_name="bitacora.db"):
        self.connection = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        queries = [
            """CREATE TABLE IF NOT EXISTS bitacora (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TEXT,
                supervisor TEXT,
                descripcion TEXT,
                anexos TEXT,
                responsable TEXT,
                clima TEXT
            )""",
            """CREATE TABLE IF NOT EXISTS actividades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TEXT,
                supervisor TEXT,
                descripcion TEXT,
                anexos TEXT,
                responsable TEXT,
                clima TEXT
            )""",
            """CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT,
                correo TEXT UNIQUE,
                contrasena TEXT
            )"""
        ]
        for query in queries:
            self.execute_query(query)

    def execute_query(self, query, params=()):
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        self.connection.commit()
        return cursor

    def fetch_query(self, query, params=()):
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()

    def clear_tables(self):
        queries = [
            "DELETE FROM bitacora",
            "DELETE FROM actividades",
            "DELETE FROM usuarios"
        ]
        for query in queries:
            self.execute_query(query)

    def close_connection(self):
        self.connection.close()
