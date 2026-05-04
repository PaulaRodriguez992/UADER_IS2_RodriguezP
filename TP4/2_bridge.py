#*------------------------------------------------------------------------
#* Ingeniería de Software II
#* Patrones Estructurales
#* Bridge - TP4 Punto 2
#* UADER - Ingeniería de Software II
#*------------------------------------------------------------------------

# El patrón Bridge separa una abstracción de su implementación,
# de modo que ambas puedan cambiar de forma independiente.
#
# En este ejemplo:
#   Abstracción  → Lamina (el producto, con sus atributos fijos)
#   Implementación → TrenLaminador (la forma concreta de producirla)
#
# Sin Bridge, agregar un tercer tren obligaría a modificar Lamina.
# Con Bridge, solo se agrega una nueva subclase de TrenLaminador.

from abc import ABC, abstractmethod
import platform
import os

# -----------------------------------------------------------------------------
# IMPLEMENTACIÓN: jerarquía de trenes laminadores
# -----------------------------------------------------------------------------

class TrenLaminador(ABC):
    """
    Interfaz de implementación.
    Define el contrato que deben cumplir todos los trenes laminadores.
    Lamina depende de esta interfaz, no de los trenes concretos.
    """

    @abstractmethod
    def producir(self, espesor: float, ancho: float) -> None:
        """Produce una plancha con el espesor y ancho dados."""
        pass


class TrenLaminador5m(TrenLaminador):
    """
    Implementación concreta A.
    Tren que genera planchas de 5 metros de largo.
    """

    def producir(self, espesor: float, ancho: float) -> None:
        print(f"[Tren 5m] Produciendo plancha: {espesor}\" espesor x {ancho}m ancho x 5m largo")


class TrenLaminador10m(TrenLaminador):
    """
    Implementación concreta B.
    Tren que genera planchas de 10 metros de largo.
    """

    def producir(self, espesor: float, ancho: float) -> None:
        print(f"[Tren 10m] Produciendo plancha: {espesor}\" espesor x {ancho}m ancho x 10m largo")


# -----------------------------------------------------------------------------
# ABSTRACCIÓN: la lámina de acero
# -----------------------------------------------------------------------------

class Lamina:
    """
    Abstracción.
    Representa la lámina de acero con sus atributos fijos (espesor y ancho).
    No sabe cómo producirse; le delega esa responsabilidad al tren
    que recibe como parámetro → ese es el 'puente' (bridge).

    Ventaja: si mañana aparece un TrenLaminador20m, solo se agrega esa clase.
    Lamina no necesita ningún cambio.
    """

    def __init__(self, espesor: float, ancho: float, tren: TrenLaminador) -> None:
        self._espesor = espesor   # atributo fijo del producto
        self._ancho = ancho       # atributo fijo del producto
        self._tren = tren         # referencia al tren (la implementación)

    def producir(self) -> None:
        """
        Delega la producción al tren asignado.
        La lámina no conoce los detalles internos del tren.
        """
        self._tren.producir(self._espesor, self._ancho)

    def cambiar_tren(self, tren: TrenLaminador) -> None:
        """
        Permite reasignar el tren en tiempo de ejecución.
        Esto muestra una ventaja clave del Bridge: la implementación
        puede cambiarse sin tocar la abstracción ni crear un objeto nuevo.
        """
        self._tren = tren
        print("[Lamina] Tren laminador actualizado.")


# =============================================================================
# Punto de entrada
# =============================================================================

if __name__ == "__main__":
    os.system("cls" if platform.system() == "Windows" else "clear")

    # Se instancian los dos trenes disponibles (las implementaciones)
    tren5  = TrenLaminador5m()
    tren10 = TrenLaminador10m()

    print("=== Lámina enviada al tren de 5m ===")
    # La lámina recibe el tren en el constructor → ese es el puente
    lamina = Lamina(espesor=0.5, ancho=1.5, tren=tren5)
    lamina.producir()

    print("\n=== Lámina enviada al tren de 10m ===")
    # Otra lámina con los mismos atributos pero distinto tren
    lamina2 = Lamina(espesor=0.5, ancho=1.5, tren=tren10)
    lamina2.producir()

    print("\n=== Cambio de tren en tiempo de ejecución ===")
    # La misma instancia de lamina ahora usa el tren de 10m
    lamina.cambiar_tren(tren10)
    lamina.producir()