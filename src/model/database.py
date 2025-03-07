import sqlite3

class Database:
    def __init__(self, db_name="bitacora.db"):
        """Inicializa la conexión a la base de datos."""
        pass

    def create_tables(self):
        """Crea las tablas necesarias para la gestión de la bitácora."""
        pass

    def execute_query(self, query, params=()):
        """Ejecuta una consulta que modifica la base de datos."""
        pass

    def fetch_query(self, query, params=()):
        """Ejecuta una consulta que recupera datos de la base de datos."""
        pass

    def close_connection(self):
        """Cierra la conexión con la base de datos."""
        pass
