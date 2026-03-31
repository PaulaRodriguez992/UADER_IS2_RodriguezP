#!/usr/bin/python
#*-------------------------------------------------------------------------*
#* factorial_OOP.py                                                        *
#* calcula el factorial usando programación orientada a objetos            *
#* Dr.P.E.Colla (c) 2022                                                   *
#* Creative commons                                                        *
#*-------------------------------------------------------------------------*
import sys

class Factorial:
    """Clase que implementa el cálculo de factorial usando OOP"""

    def __init__(self):
        """Constructor de la clase Factorial"""
        pass

    def factorial(self, num):
        """Calcula el factorial de un número entero positivo"""
        if num < 0:
            # El factorial no está definido para números negativos
            print("Factorial de un número negativo no existe")
            return 0
        elif num == 0:
            # Por definición, el factorial de 0 es 1
            return 1
        else:
            # Cálculo iterativo del factorial
            fact = 1
            while(num > 1):
                fact *= num   # Multiplica acumulando el resultado
                num -= 1      # Decrementa el número en cada iteración
            return fact

    def run(self, min, max):
        """Calcula e imprime el factorial de todos los números entre min y max"""
        for num in range(min, max + 1):
            print("Factorial ", num, "! es ", self.factorial(num))

# Verificar si se pasó un argumento por línea de comandos
if len(sys.argv) < 2:
    # Si no hay argumento, solicitarlo al usuario interactivamente
    entrada = input("Ingrese un número o rango (ej. 4-8, -10, 5-): ")
else:
    # Tomar el argumento pasado por línea de comandos
    entrada = sys.argv[1]

# Crear instancia de la clase Factorial
f = Factorial()

# Determinar el tipo de entrada y ejecutar el cálculo correspondiente
if entrada.startswith("-"):
    # Caso "-hasta": calcular desde 1 hasta el número indicado
    hasta = int(entrada[1:])
    f.run(1, hasta)

elif entrada.endswith("-"):
    # Caso "desde-": calcular desde el número indicado hasta 60
    desde = int(entrada[:-1])
    f.run(desde, 60)

elif "-" in entrada:
    # Caso "desde-hasta": calcular entre ambos extremos
    partes = entrada.split("-")
    desde = int(partes[0])  # Convertir límite inferior a entero
    hasta = int(partes[1])  # Convertir límite superior a entero
    f.run(desde, hasta)

else:
    # Caso número simple
    num = int(entrada)
    f.run(num, num)