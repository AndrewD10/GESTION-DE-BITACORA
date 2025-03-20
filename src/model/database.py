import sqlite3

class Database:
    def __init__(self, db_name="bitacora.db"):
        """Inicializa la conexión a la base de datos."""
        self.db_name = db_name  # Guarda el nombre de la base de datos en el objeto
        self.connection = sqlite3.connect(self.db_name)  # Usa self.db_name
        self.cursor = self.connection.cursor()  # Crea un cursor para ejecutar consultas
        self.create_tables()  # Crea las tablas al iniciar

    def create_tables(self):
        """Crea las tablas necesarias para la gestión de la bitácora."""
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
        """Ejecuta una consulta que modifica la base de datos."""
        self.cursor.execute(query, params)
        self.connection.commit()
        return self.cursor

    def fetch_query(self, query, params=()):
        """Ejecuta una consulta que recupera datos de la base de datos."""
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def clear_tables(self):
        """Elimina todos los datos de las tablas sin borrar la estructura."""
        queries = [
            "DELETE FROM bitacora",
            "DELETE FROM actividades",
            "DELETE FROM usuarios"
        ]
        for query in queries:
            self.execute_query(query)

    def close_connection(self):
        """Cierra la conexión con la base de datos."""
        self.connection.close()
