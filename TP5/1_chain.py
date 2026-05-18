#*------------------------------------------------------------------------
#* Ingeniería de Software II
#* Patrones de Comportamiento
#* Chain of Responsibility - TP5 Punto 1
#* UADER - Ingeniería de Software II
#* Rodriguez Paula
#*------------------------------------------------------------------------

import os
import platform


class ManejadorNumero:
    """
    Handler abstracto base.
    Define la cadena: cada handler tiene referencia al siguiente.
    Si no puede procesar el número, lo pasa al siguiente.
    """

    def __init__(self):
        self._siguiente = None

    def establecer_siguiente(self, siguiente):
        self._siguiente = siguiente
        return siguiente  # permite encadenar en una sola línea

    def manejar(self, numero):
        """Intenta procesar. Si no puede, pasa al siguiente."""
        if not self.procesar(numero):
            if self._siguiente:
                self._siguiente.manejar(numero)

    def procesar(self, numero):
        """Cada subclase define su criterio. Devuelve True si consumió el número."""
        raise NotImplementedError


class ManejadorPrimos(ManejadorNumero):
    """
    Consume el número si es primo.
    Va primero en la cadena: los primos nunca llegan al manejador de pares.
    """

    def _es_primo(self, n):
        if n < 2:
            return False
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                return False
        return True

    def procesar(self, numero):
        if self._es_primo(numero):
            print(f"[Primos]  {numero:>3} → consumido (primo)")
            return True
        return False


class ManejadorPares(ManejadorNumero):
    """
    Consume el número si es par.
    Solo recibe los que no fueron primos (el 2 ya fue tomado por ManejadorPrimos).
    """

    def procesar(self, numero):
        if numero % 2 == 0:
            print(f"[Pares]   {numero:>3} → consumido (par)")
            return True
        return False


class ManejadorDefault(ManejadorNumero):
    """
    Último eslabón de la cadena.
    Marca como no consumido todo lo que llegue hasta acá
    (impares no primos: 1, 9, 15, 21, 25...).
    """

    def procesar(self, numero):
        print(f"[Default] {numero:>3} → no consumido")
        return True


if __name__ == "__main__":
    os.system("cls" if platform.system() == "Windows" else "clear")

    # Construcción de la cadena: primos → pares → default
    primos  = ManejadorPrimos()
    pares   = ManejadorPares()
    default = ManejadorDefault()

    primos.establecer_siguiente(pares)
    pares.establecer_siguiente(default)

    print("=== Procesando números del 1 al 100 ===\n")
    for numero in range(1, 101):
        primos.manejar(numero)