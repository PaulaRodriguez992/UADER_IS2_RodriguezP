#*------------------------------------------------------------------------
#* Ingeniería de Software II
#* Patrones Estructurales
#* Composite - TP4 Punto 3
#* UADER - Ingeniería de Software II
#*------------------------------------------------------------------------

# El patrón Composite organiza objetos en una estructura de árbol.
# La idea central es que el cliente puede tratar un objeto simple
# y un grupo de objetos de la misma manera, usando una interfaz común.
#
# En este ejemplo:
#   Componente  → ComponenteEnsamblado (interfaz abstracta común)
#   Hoja        → Pieza (no tiene hijos, es el nivel más bajo)
#   Composite   → SubConjunto / ProductoPrincipal (contiene otros componentes)

from abc import ABC, abstractmethod
import platform
import os

# -----------------------------------------------------------------------------
# COMPONENTE ABSTRACTO: interfaz común para hojas y compuestos
# -----------------------------------------------------------------------------

class ComponenteEnsamblado(ABC):
    """
    Interfaz común.
    Tanto Pieza como SubConjunto implementan este contrato.
    Esto permite que el cliente llame a mostrar() en cualquiera
    sin saber si es una pieza simple o un subconjunto con hijos.
    """

    @abstractmethod
    def mostrar(self, indentacion: int = 0) -> None:
        pass


# -----------------------------------------------------------------------------
# HOJA: nivel más bajo del árbol, no tiene hijos
# -----------------------------------------------------------------------------

class Pieza(ComponenteEnsamblado):
    """
    Hoja del árbol Composite.
    Representa una pieza individual sin componentes internos.
    Implementa mostrar() directamente, sin iterar sobre hijos.
    """

    def __init__(self, nombre: str) -> None:
        self.nombre = nombre

    def mostrar(self, indentacion: int = 0) -> None:
        # Imprime la pieza con la sangría correspondiente a su nivel en el árbol
        print(" " * indentacion + f"- Pieza: {self.nombre}")


# -----------------------------------------------------------------------------
# COMPOSITE: nodo intermedio que puede contener hojas u otros composites
# -----------------------------------------------------------------------------

class SubConjunto(ComponenteEnsamblado):
    """
    Nodo compuesto.
    Puede contener Piezas u otros SubConjuntos.
    Al llamar a mostrar(), se muestra a sí mismo y luego
    llama recursivamente a mostrar() en cada hijo.
    Esa recursión es la clave del patrón Composite.
    """

    def __init__(self, nombre: str, opcional: bool = False) -> None:
        self.nombre = nombre
        self.opcional = opcional          # indica si es el subconjunto optativo
        self._componentes: list[ComponenteEnsamblado] = []   # lista de hijos

    def agregar(self, componente: ComponenteEnsamblado) -> None:
        """Agrega un hijo (pieza u otro subconjunto) a este nodo."""
        self._componentes.append(componente)

    def remover(self, componente: ComponenteEnsamblado) -> None:
        """Elimina un hijo de este nodo."""
        self._componentes.remove(componente)

    def mostrar(self, indentacion: int = 0) -> None:
        etiqueta = " [OPCIONAL]" if self.opcional else ""
        print(" " * indentacion + f"+ SubConjunto: {self.nombre}{etiqueta}")
        # Llama recursivamente a mostrar() en cada componente hijo
        for componente in self._componentes:
            componente.mostrar(indentacion + 4)   # +4 aumenta la sangría


# -----------------------------------------------------------------------------
# RAÍZ: el nivel más alto del árbol
# -----------------------------------------------------------------------------

class ProductoPrincipal(ComponenteEnsamblado):
    """
    Nodo raíz del árbol de ensamblado.
    Funciona igual que SubConjunto pero representa el producto completo.
    Contiene subconjuntos y los muestra recursivamente.
    """

    def __init__(self, nombre: str) -> None:
        self.nombre = nombre
        self._subconjuntos: list[ComponenteEnsamblado] = []

    def agregar(self, subconjunto: ComponenteEnsamblado) -> None:
        self._subconjuntos.append(subconjunto)

    def remover(self, subconjunto: ComponenteEnsamblado) -> None:
        self._subconjuntos.remove(subconjunto)

    def mostrar(self, indentacion: int = 0) -> None:
        print(" " * indentacion + f"* Producto: {self.nombre}")
        # Delega a cada subconjunto, que a su vez delegará a sus piezas
        for subconjunto in self._subconjuntos:
            subconjunto.mostrar(indentacion + 4)

# =============================================================================
# Punto de entrada
# =============================================================================

if __name__ == "__main__":
    os.system("cls" if platform.system() == "Windows" else "clear")

    # Se construye el árbol de abajo hacia arriba:
    # primero las hojas (piezas), luego los nodos (subconjuntos), luego la raíz

    producto = ProductoPrincipal("Ensamblado Principal")

    # Subconjunto 1 con 4 piezas
    sc1 = SubConjunto("SubConjunto 1")
    for i in range(1, 5):
        sc1.agregar(Pieza(f"Pieza 1.{i}"))

    # Subconjunto 2 con 4 piezas
    sc2 = SubConjunto("SubConjunto 2")
    for i in range(1, 5):
        sc2.agregar(Pieza(f"Pieza 2.{i}"))

    # Subconjunto 3 con 4 piezas
    sc3 = SubConjunto("SubConjunto 3")
    for i in range(1, 5):
        sc3.agregar(Pieza(f"Pieza 3.{i}"))

    # Se conectan los subconjuntos al producto principal (raíz del árbol)
    producto.agregar(sc1)
    producto.agregar(sc2)
    producto.agregar(sc3)

    print("=== Estructura inicial (3 subconjuntos) ===\n")
    # mostrar() en la raíz recorre todo el árbol recursivamente
    producto.mostrar()

    # Se agrega el subconjunto opcional sin modificar ninguna clase existente
    # Eso demuestra la flexibilidad del patrón Composite
    sc_op = SubConjunto("SubConjunto Opcional", opcional=True)
    for i in range(1, 5):
        sc_op.agregar(Pieza(f"Pieza O.{i}"))

    producto.agregar(sc_op)

    print("\n=== Estructura final (con subconjunto opcional) ===\n")
    producto.mostrar()