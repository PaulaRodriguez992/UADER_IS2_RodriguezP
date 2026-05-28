import os
import sys

# Valores iniciales por defecto (no se usan en esta versión real)
lower = 1 
upper = 50

# Muestra la cantidad de argumentos recibidos
print("La cantidad de argumentos es %d\n" % len(sys.argv))

# Muestra el nombre del script
print("El programa que ejecuta se llama %s" % sys.argv[0])

# Toma los argumentos desde línea de comandos para definir el rango de búsqueda
# Convierte los argumentos (strings) a enteros
lower = int(sys.argv[1])
upper = int(sys.argv[2])

print("Los argumentos que recibí fueron %d y %d" % (lower, upper))

# Limpia la pantalla (solo funciona en sistemas tipo Unix, usar 'cls' en Windows)
os.system('clear')

# Informa el rango de búsqueda
print('Números primos entre %d y %d son: \n' % (lower, upper))

# Búsqueda de números primos en el rango especificado
for num in range(lower, upper + 1):
    if num > 1:  # Los primos son mayores que 1
        for i in range(2, num):  # Verifica si num tiene divisores
            if num % i == 0:
                break  # No es primo
        else:
            print('%d ' % num)  # Es primo

