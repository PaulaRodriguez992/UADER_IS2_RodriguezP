import json
import os
import random
from itertools import permutations

# Ruta del archivo donde se guardará el historial de pares generados
HISTORIAL_PATH = "pares_generados.json"

# Número máximo de pares únicos que se mantendrán en la memoria del historial
MAX_HISTORIAL = 10

def es_primo(n):
    """Retorna True si n es un número primo, False en caso contrario."""
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):  # Optimización: solo hasta la raíz cuadrada
        if n % i == 0:
            return False
    return True

def obtener_primos_hasta_100():
    """Devuelve una lista de todos los números primos entre 2 y 100."""
    return [n for n in range(2, 101) if es_primo(n)]

def cargar_historial():
    """Carga el historial desde un archivo JSON, si existe."""
    if os.path.exists(HISTORIAL_PATH):
        with open(HISTORIAL_PATH, "r") as f:
            return json.load(f)
    return []  # Si no existe, retorna una lista vacía

def guardar_historial(historial):
    """Guarda el historial actualizado en el archivo JSON."""
    with open(HISTORIAL_PATH, "w") as f:
        json.dump(historial, f)

def generar_par_no_repetido(primos, historial):
    """
    Elige aleatoriamente un par de números primos que no haya sido usado antes.
    Los pares (a, b) y (b, a) se consideran distintos.
    """
    pares_posibles = list(permutations(primos, 2))  # Todos los pares posibles sin repetición
    random.shuffle(pares_posibles)  # Los mezcla al azar

    for par in pares_posibles:
        if list(par) not in historial:
            return list(par)  # Devuelve un nuevo par no repetido
    
    # Si no hay pares nuevos disponibles
    raise Exception("No quedan pares únicos disponibles entre los primos.")

def actualizar_historial(historial, nuevo_par):
    """Agrega el nuevo par al historial y mantiene solo los últimos 10 pares."""
    historial.append(nuevo_par)
    if len(historial) > MAX_HISTORIAL:
        historial.pop(0)  # Elimina el par más antiguo
    return historial

def generar_clave():
    """
    Función principal que:
    - Obtiene los primos entre 2 y 100.
    - Carga historial de pares anteriores.
    - Genera un nuevo par único.
    - Calcula su producto como clave.
    - Actualiza y guarda el historial.
    """
    primos = obtener_primos_hasta_100()
    historial = cargar_historial()
    
    nuevo_par = generar_par_no_repetido(primos, historial)
    historial = actualizar_historial(historial, nuevo_par)
    guardar_historial(historial)

    p, q = nuevo_par
    clave = p * q
    print(f"Par seleccionado: {p}, {q}")
    print(f"Clave generada: {clave}")

# Punto de entrada principal del script
if __name__ == "__main__":
    generar_clave()
