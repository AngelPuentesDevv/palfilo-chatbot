from flask import Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from chatbot_service import app as chatbot_app
from MicroServicioWebScraping import app as scraping_app

# Crear una aplicación principal
app = Flask(__name__)

# Registrar ambas aplicaciones como subaplicaciones
app.wsgi_app = DispatcherMiddleware(
    app.wsgi_app,
    {
        "/chatbot": chatbot_app,  # Rutas del chatbot
        "/scraping": scraping_app,  # Rutas del servicio de scraping
    },
)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
