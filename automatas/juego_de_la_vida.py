import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QSlider
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import QTimer, Qt

class JuegoVida(QWidget):
    def __init__(self, filas=20, columnas=20, tamaño_celda=20):
        super().__init__()
        self.filas = filas
        self.columnas = columnas
        self.tamaño_celda = tamaño_celda
        self.tablero = np.random.randint(2, size=(filas, columnas))

        # Temporizador para actualizar el tablero
        self.temporizador = QTimer()
        self.temporizador.timeout.connect(self.actualizar_tablero)

        # Configuración ventana
        self.setWindowTitle("Juego de la Vida Mejorado")
        self.resize(columnas * tamaño_celda + 200, filas * tamaño_celda + 50)

        # Layout principal
        self.layout_principal = QHBoxLayout()
        self.setLayout(self.layout_principal)

        # Área de tablero
        self.tablero_widget = QWidget()
        self.tablero_widget.setFixedSize(columnas * tamaño_celda, filas * tamaño_celda)
        self.layout_principal.addWidget(self.tablero_widget)

        # Panel de controles
        self.panel_controles = QVBoxLayout()
        self.layout_principal.addLayout(self.panel_controles)

        # Botones
        self.btn_iniciar = QPushButton("Iniciar")
        self.btn_iniciar.clicked.connect(self.iniciar)
        self.panel_controles.addWidget(self.btn_iniciar)

        self.btn_pausar = QPushButton("Pausar")
        self.btn_pausar.clicked.connect(self.pausar)
        self.panel_controles.addWidget(self.btn_pausar)

        self.btn_reiniciar = QPushButton("Reiniciar")
        self.btn_reiniciar.clicked.connect(self.reiniciar)
        self.panel_controles.addWidget(self.btn_reiniciar)

        # Slider velocidad
        self.label_vel = QLabel("Velocidad: 1.8s")
        self.panel_controles.addWidget(self.label_vel)

        self.slider_vel = QSlider(Qt.Horizontal)
        self.slider_vel.setMinimum(1)
        self.slider_vel.setMaximum(10)
        self.slider_vel.setValue(2)
        self.slider_vel.valueChanged.connect(self.cambiar_velocidad)
        self.panel_controles.addWidget(self.slider_vel)

        # Estado
        self.corriendo = False

    def iniciar(self):
        if not self.corriendo:
            self.temporizador.start(int(self.slider_vel.value()*1000))
            self.corriendo = True

    def pausar(self):
        self.temporizador.stop()
        self.corriendo = False

    def reiniciar(self):
        self.tablero = np.random.randint(2, size=(self.filas, self.columnas))
        self.update()

    def cambiar_velocidad(self):
        self.label_vel.setText(f"Velocidad: {self.slider_vel.value()}s")
        if self.corriendo:
            self.temporizador.start(int(self.slider_vel.value()*1000))

    def actualizar_tablero(self):
        nuevo_tablero = np.copy(self.tablero)
        for f in range(self.filas):
            for c in range(self.columnas):
                vecinos = np.sum(self.tablero[max(0, f-1):min(f+2, self.filas),
                                              max(0, c-1):min(c+2, self.columnas)]) - self.tablero[f, c]
                # Reglas de Conway
                if self.tablero[f, c] == 1 and (vecinos < 2 or vecinos > 3):
                    nuevo_tablero[f, c] = 0
                elif self.tablero[f, c] == 0 and vecinos == 3:
                    nuevo_tablero[f, c] = 1
        self.tablero = nuevo_tablero
        self.update()

    def paintEvent(self, event):
        pintor = QPainter(self)
        for f in range(self.filas):
            for c in range(self.columnas):
                x = c * self.tamaño_celda
                y = f * self.tamaño_celda
                color = QColor(0, 200, 0) if self.tablero[f, c] == 1 else QColor(255, 255, 255)
                pintor.fillRect(x, y, self.tamaño_celda, self.tamaño_celda, color)
                pintor.setPen(QColor(200, 200, 200))
                pintor.drawRect(x, y, self.tamaño_celda, self.tamaño_celda)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = JuegoVida()
    ventana.show()
    sys.exit(app.exec_())
