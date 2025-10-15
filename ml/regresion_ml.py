import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error

ARCHIVO_DATOS = "datos_casas.txt"


# Funciones auxiliares

def crear_datos_iniciales():
    """Crea un archivo con datos iniciales si no existe."""
    datos_iniciales = [
        (50, 100),
        (70, 140),
        (100, 200),
        (120, 240),
        (150, 300)
    ]
    guardar_datos(datos_iniciales)
    print(f"Archivo '{ARCHIVO_DATOS}' creado con datos iniciales.\n")

def leer_datos():
    """Lee los datos desde el archivo, crea iniciales si no existe."""
    if not os.path.exists(ARCHIVO_DATOS):
        crear_datos_iniciales()
    datos = []
    with open(ARCHIVO_DATOS, "r") as f:
        for linea in f:
            try:
                tamaño, precio = map(float, linea.strip().split())
                datos.append((tamaño, precio))
            except ValueError:
                continue
    return datos

def guardar_datos(datos):
    """Guarda los datos en el archivo."""
    with open(ARCHIVO_DATOS, "w") as f:
        for tamaño, precio in datos:
            f.write(f"{tamaño} {precio}\n")
    print("Datos guardados correctamente.\n")

def mostrar_datos(datos):
    """Muestra los datos cargados."""
    if not datos:
        print("No hay datos disponibles.\n")
        return
    print("\n=== Datos cargados ===")
    for tamaño, precio in datos:
        print(f"  Tamaño: {tamaño} m² → Precio: {precio} mil dólares")
    print()
    
# Modelo y predicción

def entrenar_modelo(datos):
    """Entrena un modelo de regresión lineal."""
    if len(datos) < 2:
        print("Se necesitan al menos 2 datos para entrenar el modelo.\n")
        return None

    X = np.array([[d[0]] for d in datos])
    y = np.array([d[1] for d in datos])

    modelo = LinearRegression()
    modelo.fit(X, y)
    y_pred = modelo.predict(X)

    print(" Modelo entrenado correctamente:")
    print(f"  Pendiente (m): {modelo.coef_[0]:.2f}")
    print(f"  Intersección (b): {modelo.intercept_:.2f}")
    print(f"  Coeficiente de determinación R²: {r2_score(y, y_pred):.4f}")
    print(f"  Error cuadrático medio MSE: {mean_squared_error(y, y_pred):.2f}\n")

    graficar_modelo(modelo, datos)
    return modelo

def predecir(modelo, tamaño, datos):
    """Realiza predicción y advierte si se extrapola fuera del rango."""
    if modelo is None:
        print("El modelo no está entrenado.\n")
        return
    tamaños = [d[0] for d in datos]
    if tamaño < min(tamaños) or tamaño > max(tamaños):
        print("⚠️  Advertencia: tamaño fuera del rango de entrenamiento.")
    prediccion = modelo.predict([[tamaño]])[0]
    print(f"\nPredicción: Casa de {tamaño} m² → {prediccion:.2f} mil dólares\n")


# Gráficos

def graficar_modelo(modelo, datos):
    """Grafica los datos reales y la línea de regresión."""
    X = np.array([[d[0]] for d in datos])
    y = np.array([d[1] for d in datos])
    y_pred = modelo.predict(X)

    plt.figure(figsize=(8,5))
    plt.scatter(X, y, color='blue', label='Datos reales')
    plt.plot(X, y_pred, color='red', linewidth=2, label='Modelo lineal')
    for i, (xi, yi) in enumerate(zip(X, y)):
        plt.text(xi, yi+2, f"({xi[0]}, {yi})", fontsize=8)
    plt.xlabel("Tamaño (m²)")
    plt.ylabel("Precio (mil dólares)")
    plt.title("Regresión Lineal - Precio vs Tamaño")
    plt.legend()
    plt.grid(True)
    plt.show()


# Menú principal

def regresion_ml():
    print("=== REGRESIÓN LINEAL: Predicción de precios de casas ===\n")
    datos = leer_datos()
    modelo = entrenar_modelo(datos)

    while True:
        print("\nOpciones disponibles:")
        print("  1. Ver datos")
        print("  2. Agregar nuevo dato (tamaño, precio)")
        print("  3. Entrenar modelo")
        print("  4. Predecir precio")
        print("  5. Ver ruta del archivo")
        print("  6. Salir\n")

        opcion = input("Seleccione una opción (1-6): ").strip()
        if opcion == "1":
            mostrar_datos(datos)
        elif opcion == "2":
            try:
                tamaño = float(input("Ingrese tamaño (m²): "))
                precio = float(input("Ingrese precio (en miles de dólares): "))
                datos.append((tamaño, precio))
                guardar_datos(datos)
            except ValueError:
                print("Error: Ingrese valores numéricos válidos.\n")
        elif opcion == "3":
            modelo = entrenar_modelo(datos)
        elif opcion == "4":
            try:
                tamaño = float(input("Ingrese tamaño de casa (m²): "))
                predecir(modelo, tamaño, datos)
            except ValueError:
                print("Error: valor no válido.\n")
        elif opcion == "5":
            print(f"\nArchivo de datos: {os.path.abspath(ARCHIVO_DATOS)}\n")
        elif opcion == "6":
            print("Programa finalizado.")
            break
        else:
            print("Opción no válida. Intente nuevamente.\n")
