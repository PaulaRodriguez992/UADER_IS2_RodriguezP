#!/usr/bin/python3
# Python program to display all the prime numbers within an interval

# primos.py
# Programa que calcula e imprime los números primos en un rango dado

# Definición del rango de búsqueda
lower = 1   # Límite inferior del rango
upper = 500 # Límite superior del rango

print("Prime numbers between", lower, "and", upper, "are:")

# Iteración sobre todos los números en el rango definido
for num in range(lower, upper + 1):
   # Los números primos son siempre mayores que 1
   if num > 1:
       # Verificar si el número tiene algún divisor distinto de 1 y sí mismo
       for i in range(2, num):
           # Si num es divisible por i, no es primo
           if (num % i) == 0:
               break
       else:
           # Si no se encontró ningún divisor, el número es primo
           print(num)