from datetime import datetime
from typing import Optional, List, Dict
from dataclasses import dataclass
from geoalchemy2 import Geography


@dataclass
class Restaurant:
    """Clase que representa un restaurante."""

    restaurant_id: Optional[int] = None
    name: str = ""
    address: str = ""
    location: Optional[Geography] = None
    category: Optional[str] = None
    opening_hours: Optional[Dict] = None
    menu_url: Optional[str] = None
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    def to_dict(self) -> dict:
        """Convierte el objeto a un diccionario."""
        return {
            "restaurant_id": self.restaurant_id,
            "name": self.name,
            "address": self.address,
            "category": self.category,
            "opening_hours": self.opening_hours,
            "menu_url": self.menu_url,
        }
