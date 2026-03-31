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
   entrada = input("Ingrese un número o rango (ej. 4-8): ")
else:
   entrada = sys.argv[1]

# Verificar si es un rango desde-hasta
if "-" in entrada:
    partes = entrada.split("-")
    desde = int(partes[0])
    hasta = int(partes[1])
    for num in range(desde, hasta + 1):
        print("Factorial ", num, "! es ", factorial(num))
else:
    num = int(entrada)
    print("Factorial ", num, "! es ", factorial(num))