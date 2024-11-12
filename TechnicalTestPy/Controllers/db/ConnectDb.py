import sqlite3

class ConnectDb:
    def __init__(self, dbPath):
        self.dbPath = dbPath

    def connect_sqlite(self):
        try:
            # Conectar a la base de datos SQLite (si no existe, la crea)
            conn = sqlite3.connect(self.dbPath)
            return conn
        except sqlite3.Error as err:
            print(f"Error de conexión: {err}")
            return None

    def close_connection(self, conn):
        if conn:
            conn.close()
            print("Conexión cerrada")
