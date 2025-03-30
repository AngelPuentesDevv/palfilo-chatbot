import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os

# Cargar variables de entorno desde el archivo .env
load_dotenv()


class DatabaseConnection:
    """Clase Singleton para manejar la conexión a PostgreSQL."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "connection"):
            try:
                self.connection = psycopg2.connect(
                    host=os.getenv("DB_HOST"),
                    port=os.getenv("DB_PORT"),
                    database=os.getenv("DB_NAME"),
                    user=os.getenv("DB_USER"),
                    password=os.getenv("DB_PASSWORD"),
                    cursor_factory=RealDictCursor,
                )
                print("✅ Conexión a base de datos establecida")
            except Exception as e:
                print(f"❌ Error al conectar a la base de datos: {e}")
                raise e

    def __enter__(self):
        """Devuelve la conexión al entrar en el contexto."""
        return self.connection

    def __exit__(self, exc_type, exc_value, traceback):
        """Cierra la conexión al salir del contexto."""
        if self.connection:
            self.connection.close()
            print("✅ Conexión a base de datos cerrada")

    def get_connection(self):
        """Devuelve la conexión a la base de datos."""
        return self.connection
