from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Lista de etiquetas HTML relevantes para buscar la palabra clave
TAGS_TO_SEARCH = [
    "p",
    "div",
    "span",
    "article",
    "section",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
]


def scrape_site(url):
    """
    Extrae los fragmentos de texto de un sitio web donde aparece la palabra clave "menu",
    buscando en etiquetas, clases y atributos id.
    """
    try:
        response = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        if response.status_code != 200:
            return {"url": url, "error": f"HTTP {response.status_code}"}

        soup = BeautifulSoup(response.text, "html.parser")
        extracted_texts = []

        # Buscar en etiquetas HTML
        for tag in TAGS_TO_SEARCH:
            elements = soup.find_all(tag)
            for element in elements:
                text = element.get_text().strip()
                if "menu" in text.lower():
                    extracted_texts.append(
                        {
                            "tag": tag,
                            "class": element.get("class", ""),
                            "id": element.get("id", ""),
                            "text": text,
                        }
                    )

        # Buscar en atributos class e id de cualquier etiqueta
        for element in soup.find_all(True):  # Encuentra cualquier etiqueta HTML
            element_class = element.get("class", "")
            element_id = element.get("id", "")

            if (
                "menu" in str(element_class).lower()
                or "menu" in str(element_id).lower()
            ):
                extracted_texts.append(
                    {
                        "tag": element.name,
                        "class": element_class,
                        "id": element_id,
                        "text": element.get_text().strip(),
                    }
                )

        return {"url": url, "matches": extracted_texts}

    except Exception as e:
        return {"url": url, "error": str(e)}


@app.route("/api/restaurant/url/<path:url>", methods=["GET"])
def scrape(url):
    """
    Endpoint que recibe una URL como parte del path y hace Web Scraping
    para buscar la palabra clave "menu".
    """

    result = scrape_site(url)

    return jsonify(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
