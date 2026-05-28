
# Ejemplo práctico de aplicación de patrón iterator
#*------------------------------------------------------------------------
#* Ingeniería de Software II
#* Patrones de Creación
#* Iterator
#* UADER - Ingeniería de Software II
#* Dr. Pedro E. Colla
#*------------------------------------------------------------------------
"""
Iterator es útil cuando se necesita:
	recorrer colecciones de forma uniforme,
	ocultar la estructura interna,
	filtrar elementos durante el recorrido,
	recorrer datos grandes sin cargarlos todos de una vez,
	representar secuencias potencialmente largas o costosas.

Iterator separa el recorrido de la estructura recorrida.
Permite visitar elementos uno por uno sin revelar cómo están almacenados.
"""

from dataclasses import dataclass
from typing import Iterator


@dataclass
class Libro:
    """Representa un libro de una biblioteca."""
    titulo: str
    autor: str
    disponible: bool


class Biblioteca:
    """
    Colección de libros.

    Internamente usa una lista, pero el cliente no necesita saberlo.
    """

    def __init__(self) -> None:
        self._libros: list[Libro] = []

    def agregar_libro(self, libro: Libro) -> None:
        self._libros.append(libro)

    def libros_disponibles(self) -> Iterator[Libro]:
        """
        Iterator concreto.

        Recorre solo los libros disponibles.
        """
        for libro in self._libros:
            if libro.disponible:
                yield libro


def main() -> None:
    biblioteca = Biblioteca()

    biblioteca.agregar_libro(Libro("Clean Code", "Robert C. Martin", True))
    biblioteca.agregar_libro(Libro("Design Patterns", "Gamma et al.", False))
    biblioteca.agregar_libro(Libro("Refactoring", "Martin Fowler", True))

    print("Libros disponibles:")

    for libro in biblioteca.libros_disponibles():
        print(f"- {libro.titulo}, de {libro.autor}")


if __name__ == "__main__":
    main()

