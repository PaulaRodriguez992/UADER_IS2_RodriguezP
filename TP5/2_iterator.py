#*------------------------------------------------------------------------
#* Ingeniería de Software II
#* Patrones de Comportamiento
#* Iterator - TP5 Punto 2
#* UADER - Ingeniería de Software II
#* Rodriguez Paula
#*------------------------------------------------------------------------

import os
import platform
from collections.abc import Iterator, Iterable


class IteradorCadena(Iterator):
    """
    Iterator concreto.
    Recorre la cadena carácter por carácter en la dirección indicada.
    Mantiene la posición actual del recorrido.
    """

    def __init__(self, cadena: str, reverso: bool = False) -> None:
        self._cadena = cadena
        self._reverso = reverso
        # Si es reverso arranca desde el último índice, si no desde el primero
        self._posicion = len(cadena) - 1 if reverso else 0

    def __next__(self) -> str:
        """
        Devuelve el siguiente carácter.
        Lanza StopIteration cuando se agota la cadena.
        """
        if self._reverso:
            if self._posicion < 0:
                raise StopIteration
            caracter = self._cadena[self._posicion]
            self._posicion -= 1
        else:
            if self._posicion >= len(self._cadena):
                raise StopIteration
            caracter = self._cadena[self._posicion]
            self._posicion += 1
        return caracter


class CadenaCaracteres(Iterable):
    """
    Colección.
    Almacena la cadena internamente y provee iteradores
    para recorrerla sin exponer su estructura.
    """

    def __init__(self, cadena: str) -> None:
        self._cadena = cadena

    def __iter__(self) -> IteradorCadena:
        """Iterador directo (izquierda a derecha)."""
        return IteradorCadena(self._cadena, reverso=False)

    def iter_reverso(self) -> IteradorCadena:
        """Iterador reverso (derecha a izquierda)."""
        return IteradorCadena(self._cadena, reverso=True)


if __name__ == "__main__":
    os.system("cls" if platform.system() == "Windows" else "clear")

    cadena = CadenaCaracteres("UADER FCYT")

    print("=== Recorrido directo ===")
    for caracter in cadena:
        print(caracter, end=" ")
    print()

    print("\n=== Recorrido reverso ===")
    for caracter in cadena.iter_reverso():
        print(caracter, end=" ")
    print()