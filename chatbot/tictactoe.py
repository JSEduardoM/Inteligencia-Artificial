# chatbot/tictactoe.py
import random

def imprimir_tablero(tablero):
    print("\n")
    for i in range(3):
        print(" | ".join(tablero[i*3:(i+1)*3]))
        if i < 2:
            print("--+---+--")
    print("\n")

def verificar_ganador(tablero, jugador):
    combinaciones = [
        [0,1,2],[3,4,5],[6,7,8],
        [0,3,6],[1,4,7],[2,5,8],
        [0,4,8],[2,4,6]
    ]
    for combo in combinaciones:
        if all(tablero[i] == jugador for i in combo):
            return True
    return False

def tablero_lleno(tablero):
    return all(c != " " for c in tablero)

def jugar_tres_en_raya():
    tablero = [" "] * 9
    print("Comienza el juego de 3 en raya contra la IA.")
    imprimir_tablero(tablero)

    while True:
        # Turno humano
        while True:
            try:
                jugada = int(input("Elige posición (1-9): ")) - 1
                if 0 <= jugada <= 8 and tablero[jugada] == " ":
                    tablero[jugada] = "X"
                    break
                else:
                    print("Posición inválida, intenta de nuevo.")
            except:
                print("Por favor, ingresa un número del 1 al 9.")
        
        imprimir_tablero(tablero)
        if verificar_ganador(tablero, "X"):
            print("¡Has ganado!")
            break
        if tablero_lleno(tablero):
            print("Es un empate")
            break

        # Turno IA
        print("Turno de la IA...")
        posibles = [i for i in range(9) if tablero[i] == " "]
        jugada_ia = random.choice(posibles)
        tablero[jugada_ia] = "O"

        imprimir_tablero(tablero)
        if verificar_ganador(tablero, "O"):
            print("La IA ha ganado")
            break
        if tablero_lleno(tablero):
            print("Es un empate")
            break
