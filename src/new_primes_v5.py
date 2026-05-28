import sys
import os
import random

def es_primo(n):
    """Retorna True si n es un número primo, False en caso contrario."""
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):  # Optimización: hasta raíz cuadrada de n
        if n % i == 0:
            return False
    return True

def obtener_primos_en_rango(inf, sup):
    """Devuelve una lista de números primos entre inf y sup (inclusive)."""
    return [n for n in range(inf, sup + 1) if es_primo(n)]

def main():
    try:
        memoria = []
        for i in range(15):
            print(memoria)    
            numeros_primos = obtener_primos_en_rango(1, 100)
            
            num1 = random.choice(numeros_primos)
            num2 = random.choice(numeros_primos)

            if(num1, num2) in memoria:
                print(f"Primos repetidos: {num1}, {num2}")
            else:
                memoria.append((num1, num2))
                if len(memoria) > 10:
                    memoria.pop(0)
                
                print(f"Primos aleatorios: {num1}, {num2}")
                print(f"Multiplicación: {num1 * num2}")
            

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

