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
    price_range: Optional[str] = None
    opening_hours: Optional[Dict] = None
    payment_methods: Optional[List[str]] = None
    photos: Optional[List[str]] = None
    menu_url: Optional[str] = None
    average_rating: float = 0.0
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    owner_id: Optional[int] = None

    def to_dict(self) -> dict:
        """Convierte el objeto a un diccionario."""
        return {
            "restaurant_id": self.restaurant_id,
            "name": self.name,
            "address": self.address,
            "category": self.category,
            "price_range": self.price_range,
            "opening_hours": self.opening_hours,
            "payment_methods": self.payment_methods,
            "photos": self.photos,
            "menu_url": self.menu_url,
            "average_rating": self.average_rating,
            "owner_id": self.owner_id,
        }
