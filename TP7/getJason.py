"""
getJason.py
Recupera el valor de una clave del archivo sitedata.json.
Uso: python3 getJason.py [clave | -v]
copyright UADER-FCyT-IS2©2024 todos los derechos reservados
"""
import json
import sys

class classSingleton:
    """Implementa el patrón Singleton."""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
class classJsonReader(classSingleton):
    """Lee claves de sitedata.json. Hereda de classSingleton."""

    JSONFILE = "sitedata.json"

    def compute(self, key):
        """Devuelve el valor de 'key' en el JSON, o None si no existe."""
        with open(self.JSONFILE, "r", encoding="utf-8") as myfile:
            data = myfile.read()
        obj = json.loads(data)
        return obj.get(key, None)
if __name__ == "__main__":

    # --- Branching by abstraction: punto de convergencia ---
    # Versión OOP (nueva): usa classJsonReader
    # Para comparar con versión procedural (vieja), ambas producen igual salida

    VERSION = "1.1"
    JSONFILE = "sitedata.json"

    # Determinar la clave a buscar
    if len(sys.argv) < 2:
        jsonkey = "token1"                    # default
    elif sys.argv[1] == "-v":
        print(f"Versión {VERSION}")
        sys.exit(0)
    else:
        jsonkey = sys.argv[1]

    # Instanciar el lector (Singleton)
    reader = classJsonReader()

    # Intentar obtener el valor
    try:
        result = reader.compute(jsonkey)
    except FileNotFoundError:
        print(f"Error: no se encontró '{JSONFILE}'.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: '{JSONFILE}' no tiene formato JSON válido.")
        sys.exit(1)

    # Validar resultado
    if result is None:
        print(f"Error: la clave '{jsonkey}' no existe en '{JSONFILE}'.")
        sys.exit(1)

    print(str(result))
    sys.exit(0)
