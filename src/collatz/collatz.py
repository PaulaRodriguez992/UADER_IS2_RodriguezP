#!/usr/bin/python
#*-------------------------------------------------------------------------*
#* collatz.py                                                              *
#* Calcula la conjetura de Collatz (3n+1) para números entre 1 y 10000   *
#* y grafica las iteraciones necesarias para converger                    *
#*-------------------------------------------------------------------------*
import matplotlib.pyplot as plt

def collatz(n):
    """Calcula cuántas iteraciones tarda el número n en converger a 1
       Conjetura de Collatz: si n es par -> n/2, si n es impar -> 3n+1"""
    iteraciones = 0
    while n != 1:
        if n % 2 == 0:
            # Si n es par, dividir por 2
            n = n // 2
        else:
            # Si n es impar, aplicar 3n+1
            n = 3 * n + 1
        iteraciones += 1
    return iteraciones

# Listas para almacenar los datos del gráfico
numeros = []
iteraciones = []

# Calcula Collatz para todos los números entre 1 y 10000
for n in range(1, 10001):
    numeros.append(n)
    iteraciones.append(collatz(n))

# gráfico
plt.figure(figsize=(14, 7))
plt.scatter(iteraciones, numeros, s=0.1, color='blue', alpha=0.5)


plt.xlabel("Número de iteraciones para converger")
plt.ylabel("Número n de inicio de la secuencia")
plt.title("Conjetura de Collatz - Números del 1 al 10000")
plt.grid(True, alpha=0.3)

# Mostrar el gráfico
plt.tight_layout()
plt.show()