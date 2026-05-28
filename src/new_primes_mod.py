import os
import sys

lower = 1

# Si se pasa un argumento por linea de comandos, se usa como limite superior.
# De lo contrario, se mantiene el comportamiento original (hasta 50).
if len(sys.argv) > 1:
    try:
        upper = int(sys.argv[1])
        if upper < 1:
            print("Error: el parametro debe ser un numero entero positivo.")
            sys.exit(1)
    except ValueError:
        print("Error: el parametro debe ser un numero entero valido.")
        sys.exit(1)
else:
    upper = 50

os.system('clear')
print('Numeros primeos entre %d y %d son: \n' % (lower, upper))

for num in range(lower, upper + 1):
    if num > 1:
        for i in range(2, num):
            if num % i == 0:
                break
        else:
            print('%d ' % num)