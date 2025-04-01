from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy import create_engine, text
from transformers import pipeline
from restaurant_dao import RestaurantDAO
from dotenv import load_dotenv
import json
import os

# Cargar variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)

# Habilitar CORS para todas las rutas
CORS(app)

# Configuración de la conexión a la base de datos
DATABASE_URL = os.getenv("DATABASE_URL")  # Cargar la URL desde la variable de entorno
if not DATABASE_URL:
    raise ValueError("DATABASE_URL no está configurada en el archivo .env")
engine = create_engine(DATABASE_URL)

# Cargar modelo de QA
qa_pipeline = pipeline(
    "question-answering",
    model="distilbert-base-cased-distilled-squad",
    max_answer_length=50,
)

print("✅ Modelo de QA cargado.")


def obtener_contexto(restaurant_id, pregunta):
    """Obtiene información específica del restaurante según la pregunta."""
    with engine.connect() as connection:
        # Consulta básica para obtener los datos del restaurante
        query = text(
            """
            SELECT name, address, category, menu_url
            FROM core.restaurants
            WHERE restaurant_id = :restaurant_id
            """
        )
        result = (
            connection.execute(query, {"restaurant_id": restaurant_id})
            .mappings()
            .fetchone()
        )
        if not result:
            return None  # Si no se encuentra el restaurante, devolver None

        # Convertir la pregunta a minúsculas para facilitar la búsqueda de palabras clave
        pregunta_lower = pregunta.lower()

        # Analizar la pregunta para determinar qué buscar
        if "dirección" in pregunta_lower:
            return result["address"]
        elif "categoría" in pregunta_lower or "tipo de comida" in pregunta_lower:
            return result["category"]
        elif "menú" in pregunta_lower:
            return result["menu_url"]  # Devolver el valor completo del campo menu_url
        else:
            return None  # Si no se encuentra una palabra clave relevante, devolver None


@app.route("/chat", methods=["POST"])
def chat():
    """Procesa la pregunta del usuario con el contexto del restaurante."""
    datos = request.get_json()
    pregunta = datos.get("pregunta", "")
    restaurant_id = datos.get("restaurant_id", None)
    print(datos)

    if not restaurant_id:
        return jsonify({"error": "Falta el ID del restaurante."}), 400

    contexto = obtener_contexto(restaurant_id, pregunta)

    if contexto == "Información no encontrada.":
        return (
            jsonify({"error": "No se encontró información sobre este restaurante."}),
            404,
        )

    respuesta = qa_pipeline({"question": pregunta, "context": contexto})
    return jsonify({"respuesta": respuesta["answer"]})


if __name__ == "__main__":
    print("🚀 Chatbot Service iniciado en http://localhost:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
