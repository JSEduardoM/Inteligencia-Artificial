# chatbot/chatbot.py
import difflib
from chatbot.tictactoe import jugar_tres_en_raya

# ===== Diccionario de respuestas =====
respuestas = {}
try:
    with open("chatbot/respuestas.txt", "r", encoding="utf-8") as f:
        for linea in f:
            if "=" in linea:
                clave, valor = linea.strip().split("=", 1)
                respuestas[clave] = valor
except FileNotFoundError:
    respuestas = {
        "hola": "Hola, aquí estoy",
        "adiós": "Que tengas un buen día.",
        "chau": "Que tengas un buen día.",
        "cómo estás": "Estoy bien, ¿y tú?",
        "tu nombre": "Soy un chatbot simple creado por GranJulio.",
        "gracias": "Aquí estaré para ti."
    }

def guardar_respuestas():
    with open("chatbot/respuestas.txt", "w", encoding="utf-8") as f:
        for clave, valor in respuestas.items():
            f.write(f"{clave}={valor}\n")

# ===== Cálculos matemáticos =====
def calcular(mensaje):
    try:
        resultado = eval(mensaje, {"__builtins__": None}, {})
        return f"El resultado es: {resultado}"
    except:
        return None

# ===== Función principal de respuesta =====
def responder(mensaje):
    mensaje = mensaje.lower()

    if "jugar 3 en raya" in mensaje or "tictactoe" in mensaje:
        jugar_tres_en_raya()
        return "Juego terminado, volvamos al chat"

    resultado = calcular(mensaje)
    if resultado:
        return resultado

    if mensaje in respuestas:
        return respuestas[mensaje]
    else:
        coincidencias = difflib.get_close_matches(mensaje, respuestas.keys(), n=1, cutoff=0.6)
        if coincidencias:
            sugerencia = coincidencias[0]
            return f"¿Quisiste decir '{sugerencia}'? {respuestas[sugerencia]}"
        else:
            print("Chatbot: No sé qué responder a eso")
            nueva_resp = input("Por favor enséñame, ¿qué debería responder?: ")
            respuestas[mensaje] = nueva_resp
            guardar_respuestas()
            return f"¡Gracias! Aprendí que a '{mensaje}' debo responder: '{nueva_resp}'"
