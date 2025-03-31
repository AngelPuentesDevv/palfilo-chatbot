from database import DatabaseConnection
import json
from psycopg2.extras import DictCursor


class RestaurantDAO:
    """Clase de acceso a datos para restaurantes."""

    def get_all_restaurants(self):
        """Obtiene todos los restaurantes."""
        query = "SELECT * FROM core.restaurants"
        try:
            with DatabaseConnection() as conn:
                with conn.cursor(cursor_factory=DictCursor) as cursor:
                    cursor.execute(query)
                    return cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener restaurantes: {e}")
            return []

    def get_restaurant_by_id(self, restaurant_id):
        """Obtiene un restaurante por su ID."""
        query = "SELECT * FROM core.restaurants WHERE restaurant_id = %s"
        try:
            with DatabaseConnection() as conn:
                with conn.cursor(cursor_factory=DictCursor) as cursor:
                    cursor.execute(query, (restaurant_id,))
                    return cursor.fetchone()
        except Exception as e:
            print(f"Error al obtener el restaurante con ID {restaurant_id}: {e}")
            return None

    def add_restaurant(self, restaurant_data):
        """Agrega un nuevo restaurante."""
        query = """
        INSERT INTO core.restaurants (
            name, address, location, category, opening_hours, menu_url
        )
        VALUES (%s, %s, ST_GeomFromText(%s, 4326), %s, %s, %s)
        RETURNING restaurant_id
        """
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        query,
                        (
                            restaurant_data["name"],
                            restaurant_data["address"],
                            restaurant_data[
                                "location"
                            ],  # WKT format (e.g., 'POINT(lon lat)')
                            restaurant_data.get("category"),
                            json.dumps(restaurant_data.get("opening_hours")),
                            restaurant_data.get("menu_url"),
                        ),
                    )
                    conn.commit()
                    return cursor.fetchone()[0]
        except Exception as e:
            print(f"Error al agregar restaurante: {e}")
            return None

    def update_restaurant(self, restaurant_id, restaurant_data):
        """Actualiza un restaurante existente."""
        query = """
        UPDATE core.restaurants
        SET name = %s, address = %s, location = ST_GeomFromText(%s, 4326),
            category = %s, opening_hours = %s, menu_url = %s,
            updated_at = CURRENT_TIMESTAMP
        WHERE restaurant_id = %s
        """
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        query,
                        (
                            restaurant_data["name"],
                            restaurant_data["address"],
                            restaurant_data["location"],  # WKT format
                            restaurant_data.get("category"),
                            json.dumps(restaurant_data.get("opening_hours")),
                            restaurant_data.get("menu_url"),
                            restaurant_id,
                        ),
                    )
                    conn.commit()
                    return cursor.rowcount > 0
        except Exception as e:
            print(f"Error al actualizar restaurante con ID {restaurant_id}: {e}")
            return False

    def delete_restaurant(self, restaurant_id):
        """Elimina un restaurante por su ID."""
        query = "DELETE FROM core.restaurants WHERE restaurant_id = %s"
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, (restaurant_id,))
                    conn.commit()
                    return cursor.rowcount > 0
        except Exception as e:
            print(f"Error al eliminar restaurante con ID {restaurant_id}: {e}")
            return False
