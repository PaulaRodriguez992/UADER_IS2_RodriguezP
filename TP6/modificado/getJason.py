"""
getJason.py
-----------
Recupera el valor de una clave desde el archivo sitedata.json.

Uso:
    python3 getJason.py [clave]

Argumentos:
    clave   Nombre de la clave a buscar en sitedata.json (default: token1)

Ejemplo:
    python3 getJason.py          -> devuelve el valor de token1
    python3 getJason.py token2   -> devuelve el valor de token2
"""

import json
import sys

JSON_FILE = 'sitedata.json'
DEFAULT_KEY = 'token1'

jsonkey = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_KEY

with open(JSON_FILE, 'r') as myfile:
    data = myfile.read()

obj = json.loads(data)

if jsonkey in obj:
    print(str(obj[jsonkey]))
else:
    print(f"Error: la clave '{jsonkey}' no existe en {JSON_FILE}")