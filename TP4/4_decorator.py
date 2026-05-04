#*------------------------------------------------------------------------
#* Ingeniería de Software II
#* Patrones Estructurales
#* Decorator - TP4 Punto 4
#* UADER - Ingeniería de Software II
#*------------------------------------------------------------------------

# El patrón Decorator agrega comportamiento a un objeto envolviéndolo,
# sin modificar su clase ni crear subclases nuevas para cada combinación.
#
# Funciona por composición en cadena:
#   cada decorador contiene una referencia al objeto que envuelve,
#   llama a su valor() y aplica su propia operación sobre ese resultado.
#
# En este ejemplo:
#   Componente base → Numero
#   Decorator base  → DecoradorNumero (envuelve cualquier Numero)
#   Decoradores concretos → SumarDos, MultiplicarPorDos, DividirPorTres

import platform
import os
# -----------------------------------------------------------------------------
# COMPONENTE BASE: el objeto que será decorado
# -----------------------------------------------------------------------------

class Numero:
    """
    Componente base.
    Almacena el número original y lo expone mediante valor().
    Es el punto de partida de cualquier cadena de decoradores.
    """

    def __init__(self, valor: float) -> None:
        self._valor = valor

    def valor(self) -> float:
        """Devuelve el valor sin ninguna transformación."""
        return self._valor

    def mostrar(self) -> None:
        print(f"Valor: {self.valor()}")

# -----------------------------------------------------------------------------
# DECORATOR BASE: envuelve un Numero y delega la llamada
# -----------------------------------------------------------------------------

class DecoradorNumero(Numero):
    """
    Decorator base.
    No aplica ninguna operación por sí mismo.
    Su función es mantener la referencia al objeto envuelto
    y definir el punto de extensión para los decoradores concretos.
    Hereda de Numero para que todos los decoradores sean intercambiables.
    """

    def __init__(self, envuelto: Numero) -> None:
        # Guarda el objeto que este decorador envuelve
        # Puede ser un Numero base u otro decorador (cadena)
        self._envuelto = envuelto

    def valor(self) -> float:
        """Delega directamente al objeto envuelto, sin modificar nada."""
        return self._envuelto.valor()


# -----------------------------------------------------------------------------
# DECORADORES CONCRETOS: cada uno aplica una operación específica
# -----------------------------------------------------------------------------

class SumarDos(DecoradorNumero):
    """
    Decorator concreto: suma 2.
    Obtiene el valor del objeto envuelto y le suma 2.
    Si envuelve otro decorador, ese resultado ya viene transformado.
    """

    def valor(self) -> float:
        return self._envuelto.valor() + 2


class MultiplicarPorDos(DecoradorNumero):
    """
    Decorator concreto: multiplica por 2.
    Obtiene el valor del objeto envuelto (que puede ser ya decorado)
    y lo multiplica por 2.
    """

    def valor(self) -> float:
        return self._envuelto.valor() * 2


class DividirPorTres(DecoradorNumero):
    """
    Decorator concreto: divide por 3.
    Obtiene el valor del objeto envuelto y lo divide por 3.
    """

    def valor(self) -> float:
        return self._envuelto.valor() / 3


# =============================================================================
# Punto de entrada
# =============================================================================

if __name__ == "__main__":
    os.system("cls" if platform.system() == "Windows" else "clear")

    numero_base = Numero(5)

    print("=== Sin decoradores ===")
    # Solo el componente base: devuelve 5
    numero_base.mostrar()

    print("\n=== Solo SumarDos ===")
    # SumarDos envuelve a Numero(5)
    # valor() → Numero.valor() + 2 = 5 + 2 = 7
    n = SumarDos(Numero(5))
    print(f"Valor: {n.valor()}")

    print("\n=== SumarDos + MultiplicarPorDos ===")
    # MultiplicarPorDos envuelve a SumarDos(Numero(5))
    # valor() → SumarDos.valor() * 2 = (5 + 2) * 2 = 14
    # La cadena se resuelve de adentro hacia afuera
    n = MultiplicarPorDos(SumarDos(Numero(5)))
    print(f"Valor: {n.valor()}")

    print("\n=== SumarDos + MultiplicarPorDos + DividirPorTres ===")
    # DividirPorTres envuelve a MultiplicarPorDos(SumarDos(Numero(5)))
    # valor() → MultiplicarPorDos.valor() / 3 = ((5 + 2) * 2) / 3 = 4.666...
    # Cada capa llama a la de adentro antes de aplicar su operación
    n = DividirPorTres(MultiplicarPorDos(SumarDos(Numero(5))))
    print(f"Valor: {n.valor()}")