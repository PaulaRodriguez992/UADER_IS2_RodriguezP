import random

MAX_HISTORIAL = 10  # Máximo número de pares recordados en memoria

def es_primo(n):
    """Retorna True si n es un número primo, False en caso contrario."""
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def obtener_primos_hasta_100():
    """Devuelve una lista de números primos entre 2 y 100."""
    primos = []  # Lista vacía para guardar los números primos
    for n in range(2, 101):  # Recorremos del 2 al 100 inclusive
        if es_primo(n):  # Si el número es primo
            primos.append(n)  # Lo agregamos a la lista
    return primos

def generar_todos_los_pares(primos):
    """Genera todos los pares posibles ordenados (a, b) con a != b."""
    pares = []
    for i in range(len(primos)):
        for j in range(len(primos)):
            if i != j:  # Evitar pares del tipo (a, a)
                pares.append([primos[i], primos[j]])
    return pares

def generar_par_no_repetido(primos, historial):
    """
    Genera un par aleatorio de números primos que no esté en el historial.
    No se repite (a, b) si ya fue generado.
    """
    pares_posibles = generar_todos_los_pares(primos)
    random.shuffle(pares_posibles)

    for par in pares_posibles:
        if par not in historial:
            return par

    raise Exception("No quedan pares únicos disponibles entre los primos.")

def actualizar_historial(historial, nuevo_par):
    """Agrega un nuevo par al historial y mantiene el tamaño máximo."""
    historial.append(nuevo_par)
    if len(historial) > MAX_HISTORIAL:
        historial.pop(0)
    return historial

def imprimir_historial(historial):
    """Imprime el historial actual de pares generados."""
    print("Historial de pares:")
    for i, par in enumerate(historial, 1):
        print(f"  {i}: ({par[0]}, {par[1]})")
    print("-" * 30)

def generar_claves_multiples(iteraciones=11):
    """Genera múltiples claves y muestra cómo evoluciona el historial."""
    primos = obtener_primos_hasta_100()
    historial = []

    for i in range(iteraciones):
        try:
            nuevo_par = generar_par_no_repetido(primos, historial)
            historial = actualizar_historial(historial, nuevo_par)
            p, q = nuevo_par
            clave = p * q
            print(f"\nIteración {i+1}: Par generado → ({p}, {q}) → Clave: {clave}")
            imprimir_historial(historial)
        except Exception as e:
            print(f"\nIteración {i+1}: Error - {e}")
            break

if __name__ == "__main__":
    generar_claves_multiples()
