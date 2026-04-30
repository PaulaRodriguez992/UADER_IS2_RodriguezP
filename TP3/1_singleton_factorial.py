#*------------------------------------------------------------------------
#* Ingeniería de Software II
#* TP3 - Patrones de Creación
#* Ejercicio 1: Factorial con Singleton
#* UADER - FCyT
#* Rodriguez Paula
#*------------------------------------------------------------------------

from threading import Lock


class CalculadorFactorial:
    """
    Singleton para el cálculo de factoriales.
    Garantiza que todas las clases que lo invoquen
    utilicen la misma instancia.
    """

    _instancia = None
    _lock = Lock()

    def __new__(cls):
        if cls._instancia is None:
            with cls._lock:
                if cls._instancia is None:   # doble verificación (thread-safe)
                    cls._instancia = super().__new__(cls)
        return cls._instancia

    def __init__(self):
        if not hasattr(self, "_inicializado"):
            self._cache = {}               # caché para evitar recalcular
            self._inicializado = True

    def calcular(self, n: int) -> int:
        """
        Retorna el factorial de n (n >= 0).
        Usa caché interna para no repetir cálculos.
        """
        if not isinstance(n, int) or n < 0:
            raise ValueError(f"El número debe ser un entero no negativo. Se recibió: {n!r}")

        if n in self._cache:
            return self._cache[n]

        resultado = 1
        for i in range(2, n + 1):
            resultado *= i

        self._cache[n] = resultado
        return resultado


# =============================================================
# Clases que usan el singleton (simulan distintos módulos
# del sistema que necesitan calcular factoriales)
# =============================================================

class ModuloEstadistica:
    def __init__(self):
        self.calc = CalculadorFactorial()   # siempre la misma instancia

    def combinaciones(self, n: int, k: int) -> int:
        """C(n, k) = n! / (k! * (n-k)!)"""
        return self.calc.calcular(n) // (
            self.calc.calcular(k) * self.calc.calcular(n - k)
        )


class ModuloMatematico:
    def __init__(self):
        self.calc = CalculadorFactorial()   # misma instancia

    def mostrar_serie(self, hasta: int) -> None:
        """Imprime n! para cada n de 0 a 'hasta'."""
        for i in range(hasta + 1):
            print(f"  {i}! = {self.calc.calcular(i)}")


# =============================================================
# main
# =============================================================

def main():
    print("=" * 50)
    print("  Ejercicio 1 — Singleton: CalculadorFactorial")
    print("=" * 50)

    # Verificación de unicidad de instancia
    inst1 = CalculadorFactorial()
    inst2 = CalculadorFactorial()
    print(f"\n¿inst1 e inst2 son la misma instancia? {inst1 is inst2}")
    print(f"  id(inst1) = {id(inst1)}")
    print(f"  id(inst2) = {id(inst2)}")

    # Uso directo
    calc = CalculadorFactorial()
    print("\n--- Cálculos directos ---")
    for n in [0, 1, 5, 10, 12]:
        print(f"  {n}! = {calc.calcular(n)}")

    # Uso desde módulos distintos
    print("\n--- Serie factorial (ModuloMatematico) ---")
    modulo_mat = ModuloMatematico()
    modulo_mat.mostrar_serie(6)

    print("\n--- Combinaciones (ModuloEstadistica) ---")
    modulo_est = ModuloEstadistica()
    print(f"  C(5,2) = {modulo_est.combinaciones(5, 2)}")
    print(f"  C(6,3) = {modulo_est.combinaciones(6, 3)}")

    # Verificar que ambos módulos usan exactamente la misma instancia
    print("\n--- Verificación de instancia compartida entre módulos ---")
    print(f"  ModuloMatematico.calc is ModuloEstadistica.calc → "
          f"{modulo_mat.calc is modulo_est.calc}")

    # Manejo de error
    print("\n--- Manejo de entrada inválida ---")
    try:
        calc.calcular(-3)
    except ValueError as e:
        print(f"  Error capturado: {e}")


if __name__ == "__main__":
    main()