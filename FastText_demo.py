import fasttext
import os
import requests
import gzip

FASTTEXT_URL = "https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/cc.es.300.bin.gz"
FASTTEXT_MODEL = "cc.es.300.bin"
FASTTEXT_GZ = "cc.es.300.bin.gz"

# --- Descarga automática del modelo preentrenado si no existe ---
def verificar_o_descargar_modelo():
    if not os.path.exists(FASTTEXT_MODEL):
        print("\n📥 Modelo preentrenado no encontrado. Iniciando descarga...")
        response = requests.get(FASTTEXT_URL, stream=True)
        with open(FASTTEXT_GZ, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        print("✅ Descarga completada. Descomprimiendo...")
        with gzip.open(FASTTEXT_GZ, "rb") as f_in, open(FASTTEXT_MODEL, "wb") as f_out:
            f_out.write(f_in.read())
        print("✅ Modelo preentrenado listo para usar.")
    else:
        print("✅ Modelo preentrenado ya disponible.")

# --- Crear archivo de entrenamiento para clasificación de texto ---
def crear_archivo_entrenamiento():
    data = """
    __label__positivo Me encantó este producto, lo volvería a comprar.
    __label__negativo No me gustó, la calidad es terrible.
    __label__positivo Muy recomendable, excelente servicio.
    __label__negativo Nunca llegó mi pedido, pésima experiencia.
    __label__positivo La entrega fue rápida y sin problemas.
    __label__negativo No funcionó como esperaba, muy decepcionado.
    """
    with open("data.txt", "w", encoding="utf-8") as f:
        f.write(data)

# --- Entrenar un modelo de clasificación de texto ---
def entrenar_modelo():
    print("\n[Entrenando modelo de clasificación de texto...]")
    modelo = fasttext.train_supervised(input="data.txt", epoch=25, lr=0.5, wordNgrams=3)
    modelo.save_model("modelo_clasificacion.bin")
    print("✅ Modelo de clasificación entrenado y guardado.")

# --- Probar el modelo de clasificación ---
def probar_modelo():
    modelo = fasttext.load_model("modelo_clasificacion.bin")
    print("\n[Probando el modelo de clasificación de texto...]")
    textos = [
        "El producto es excelente, me gustó mucho.",
        "El servicio fue muy malo, no lo recomiendo.",
        "La calidad es bastante buena, me sorprendió."
    ]
    for texto in textos:
        resultado = modelo.predict(texto)
        print(f"📝 Texto: {texto} → 🔍 Predicción: {resultado}")

# --- Probar el modelo preentrenado de FastText ---
def probar_modelo_preentrenado():
    verificar_o_descargar_modelo()
    modelo_pre = fasttext.load_model(FASTTEXT_MODEL)
    print("\n[Probando modelo preentrenado de FastText...]")
    
    palabras = ["inteligencia", "artificial", "deporte", "economía"]
    
    for palabra in palabras:
        vector = modelo_pre.get_word_vector(palabra)
        print(f"🔤 Palabra: {palabra} → 🔢 Vector (primeros 5 valores): {vector[:5]}")
          
  
        # Obtener las 5 palabras más similares
        similares = modelo_pre.get_nearest_neighbors(palabra)

        print(f"🔍 Palabras similares a '{palabra}':")
        for score, similar_word in similares:
            print(f" - {similar_word} (similitud: {score})")


# --- Ejecución del script ---
if __name__ == "__main__":
    crear_archivo_entrenamiento()
    entrenar_modelo()
    probar_modelo()
    probar_modelo_preentrenado()