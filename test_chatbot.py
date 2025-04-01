import requests

# URL del microservicio del chatbot
CHATBOT_URL = "http://localhost:5000/chat"

# Casos de prueba con preguntas sobre restaurantes
TEST_CASES = [
    # Preguntas sobre ubicación y acceso
    {
        "restaurant_id": 1,
        "pregunta": "¿Dónde está ubicado el restaurante?",
        "esperado": "dirección",
    },
    {
        "restaurant_id": 1,
        "pregunta": "¿Cuál es el horario de atención?",
        "esperado": "horario",
    },
    # Preguntas sobre pagos y precios
    {
        "restaurant_id": 1,
        "pregunta": "¿Qué métodos de pago aceptan?",
        "esperado": "pago",
    },
    {
        "restaurant_id": 1,
        "pregunta": "¿Cuál es el rango de precios?",
        "esperado": "precio",
    },
    # Preguntas sobre características del restaurante
    {
        "restaurant_id": 1,
        "pregunta": "¿Qué tipo de comida sirven?",
        "esperado": "categoría",
    },
    {
        "restaurant_id": 1,
        "pregunta": "¿Cuál es la calificación del restaurante?",
        "esperado": "rating",
    },
    # Preguntas sobre disponibilidad
    {
        "restaurant_id": 2,
        "pregunta": "¿Está abierto los domingos?",
        "esperado": "horario",
    },
    {"restaurant_id": 2, "pregunta": "¿Tienen menú digital?", "esperado": "menu"},
    # Preguntas sobre valoraciones
    {
        "restaurant_id": 2,
        "pregunta": "¿Cuántas estrellas tiene el restaurante?",
        "esperado": "rating",
    },
    {
        "restaurant_id": 2,
        "pregunta": "¿Es un restaurante costoso?",
        "esperado": "precio",
    },
]


def probar_chatbot():
    """Función para probar el chatbot de restaurantes."""
    total_preguntas = len(TEST_CASES)
    respuestas_correctas = 0

    print("🚀 Iniciando pruebas del chatbot de restaurantes...")

    for caso in TEST_CASES:
        payload = {"pregunta": caso["pregunta"], "restaurant_id": caso["restaurant_id"]}

        try:
            response = requests.post(CHATBOT_URL, json=payload)
            response_data = response.json()
            respuesta_chatbot = response_data.get("respuesta", "").strip().lower()
            esperado_lower = caso["esperado"].lower()

            # Considerar correcta si la respuesta contiene la palabra clave esperada
            es_correcto = esperado_lower in respuesta_chatbot
            if es_correcto:
                respuestas_correctas += 1

            print(f"\n🔍 Probando Restaurante ID: {caso['restaurant_id']}")
            print(f"❓ Pregunta: {caso['pregunta']}")
            print(f"💭 Respuesta: {respuesta_chatbot}")
            print(f"📝 Resultado: {'✅ Válida' if es_correcto else '❌ No válida'}")

        except Exception as e:
            print(f"⚠️ Error en la prueba: {e}")

    # Calcular y mostrar estadísticas
    porcentaje_aciertos = (respuestas_correctas / total_preguntas) * 100
    print("\n📊 Resumen de pruebas:")
    print(f"✅ Respuestas válidas: {respuestas_correctas}/{total_preguntas}")
    print(f"📈 Tasa de éxito: {porcentaje_aciertos:.2f}%")


if __name__ == "__main__":
    probar_chatbot()
