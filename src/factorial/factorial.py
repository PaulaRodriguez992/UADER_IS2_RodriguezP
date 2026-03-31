#!/usr/bin/python
#*-------------------------------------------------------------------------*
#* factorial.py                                                            *
#* calcula el factorial de un número o rango de números                   *
#* Dr.P.E.Colla (c) 2022                                                   *
#* Creative commons                                                        *
#*-------------------------------------------------------------------------*
import sys

def factorial(num): 
    if num < 0: 
        print("Factorial de un número negativo no existe")
        return 0
    elif num == 0: 
        return 1
    else: 
        fact = 1
        while(num > 1): 
            fact *= num 
            num -= 1
        return fact 

# Si no se pasó argumento, se solicita al usuario
if len(sys.argv) < 2:
   entrada = input("Ingrese un número o rango (ej. 4-8, -10, 5-): ")
else:
   entrada = sys.argv[1]

# Verificar el tipo de entrada
if entrada.startswith("-"):
    # Caso "-hasta": calcular desde 1 hasta el número indicado
    hasta = int(entrada[1:])
    for num in range(1, hasta + 1):
        print("Factorial ", num, "! es ", factorial(num))

elif entrada.endswith("-"):
    # Caso "desde-": calcular desde el número indicado hasta 60
    desde = int(entrada[:-1])
    for num in range(desde, 61):
        print("Factorial ", num, "! es ", factorial(num))

elif "-" in entrada:
    # Caso "desde-hasta": calcular entre ambos extremos
    partes = entrada.split("-")
    desde = int(partes[0])
    hasta = int(partes[1])
    for num in range(desde, hasta + 1):
        print("Factorial ", num, "! es ", factorial(num))

else:
    # Caso número simple
    num = int(entrada)
    print("Factorial ", num, "! es ", factorial(num))