# Ejemplo práctico de aplicación de patrón interpreter
#*------------------------------------------------------------------------
#* Ingeniería de Software II
#* Patrones de Creación
#* Interpreter
#* UADER - Ingeniería de Software II
#* Dr. Pedro E. Colla
#*------------------------------------------------------------------------
"""
Interpreter es útil cuando se necesita evaluar un lenguaje pequeño, estable y específico del dominio.
Casos típicos:
	reglas de negocio simples
	filtros de búsqueda
	validadores configurables
	expresiones booleanas
	mini-lenguajes de consulta
	motores de autorización
	reglas de enrutamiento

Interpreter convierte una regla en una estructura de objetos evaluable.
En lugar de codificar cada regla como un if, representamos la regla como un pequeño lenguaje que el sistema puede interpretar.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Ticket:
    """Objeto de dominio sobre el cual se evalúan reglas."""
    id: int
    prioridad: str
    estado: str
    asignado_a: str


class Expresion(ABC):
    """Interfaz común para todas las expresiones."""

    @abstractmethod
    def interpretar(self, ticket: Ticket) -> bool:
        pass


class Igual(Expresion):
    """Expresión terminal: campo = valor."""

    def __init__(self, campo: str, valor: str) -> None:
        self.campo = campo
        self.valor = valor

    def interpretar(self, ticket: Ticket) -> bool:
        return getattr(ticket, self.campo) == self.valor


class And(Expresion):
    """Expresión no terminal: expr AND expr."""

    def __init__(self, izquierda: Expresion, derecha: Expresion) -> None:
        self.izquierda = izquierda
        self.derecha = derecha

    def interpretar(self, ticket: Ticket) -> bool:
        return (
            self.izquierda.interpretar(ticket)
            and self.derecha.interpretar(ticket)
        )


class Or(Expresion):
    """Expresión no terminal: expr OR expr."""

    def __init__(self, izquierda: Expresion, derecha: Expresion) -> None:
        self.izquierda = izquierda
        self.derecha = derecha

    def interpretar(self, ticket: Ticket) -> bool:
        return (
            self.izquierda.interpretar(ticket)
            or self.derecha.interpretar(ticket)
        )


def main() -> None:
    tickets = [
        Ticket(1, "alta", "abierto", "Ana"),
        Ticket(2, "media", "abierto", "Luis"),
        Ticket(3, "alta", "cerrado", "Ana"),
        Ticket(4, "baja", "abierto", "María"),
    ]

    # Regla:
    # prioridad = alta AND estado = abierto
    regla_1 = And(
        Igual("prioridad", "alta"),
        Igual("estado", "abierto"),
    )

    # Regla:
    # asignado_a = Ana OR prioridad = baja
    regla_2 = Or(
        Igual("asignado_a", "Ana"),
        Igual("prioridad", "baja"),
    )

    print("Tickets que cumplen regla 1:")
    for ticket in tickets:
        if regla_1.interpretar(ticket):
            print(ticket)

    print("\nTickets que cumplen regla 2:")
    for ticket in tickets:
        if regla_2.interpretar(ticket):
            print(ticket)


if __name__ == "__main__":
    main()
