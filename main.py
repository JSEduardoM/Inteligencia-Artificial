import sys
from PyQt5.QtWidgets import QApplication

#Importar módulos
from chatbot.chatbot import responder, guardar_respuestas
from chatbot.tictactoe import jugar_tres_en_raya
from automatas.juego_de_la_vida import JuegoVida
from automatas.simulacion_fluido import simulacion_fluido
from grafos import grafos
from ml.regresion_ml import regresion_ml

def menu():
    while True:
        print("\n=== MENÚ PRINCIPAL ===")
        print("1. Chatbot")
        print("2. Juego de la Vida (GUI)")
        print("3. Simulación de Fluidos")
        print("4. Grafos (DFS y UCS)")
        print("5. Regresión ML")
        print("0. Salir")
        opcion = input("Elige una opción: ").strip()

        if opcion == "1":
            print("Chatbot iniciado (escribe 'salir' para terminar).")
            print("Escribe 'jugar 3 en raya' para jugar Tic-Tac-Toe contra la IA.")
            while True:
                entrada = input("Tú: ").lower()
                if entrada == "salir":
                    print("Chatbot: Adiós")
                    guardar_respuestas()
                    break
                elif entrada == "jugar 3 en raya":
                    jugar_tres_en_raya()
                else:
                    print("Chatbot:", responder(entrada))

        elif opcion == "2":
            app = QApplication(sys.argv)
            ventana = JuegoVida()
            ventana.show()
            app.exec_()

        elif opcion == "3":
            simulacion_fluido()

        elif opcion == "4":
            grafos.menu_grafos()  # Submenú de grafos

        elif opcion == "5":
            regresion_ml()

        elif opcion == "0":
            print("Saliendo del programa...")
            break

        else:
            print("Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    menu()
