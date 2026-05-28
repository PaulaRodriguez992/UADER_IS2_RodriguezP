# Ejemplo práctico de aplicación de patrón mediator
#*------------------------------------------------------------------------
#* Ingeniería de Software II
#* Patrones de Creación
#* Mediator
#* UADER - Ingeniería de Software II
#* Dr. Pedro E. Colla
#*------------------------------------------------------------------------
"""
Mediator es útil cuando muchos objetos necesitan comunicarse entre sí y se desea  evitar una red de dependencias cruzadas.

Casos típicos:

	salas de chat
	interfaces gráficas con muchos controles
	coordinación entre servicios
	sistemas de eventos
	formularios complejos
	orquestadores de workflows

Mediator evita que los objetos se comuniquen directamente entre sí.
En lugar de que todos hablen con todos, todos hablan con un coordinador común.
"""

from abc import ABC, abstractmethod


class MediadorChat(ABC):
    """Interfaz del mediador."""

    @abstractmethod
    def enviar_mensaje(self, mensaje: str, emisor: "Usuario") -> None:
        pass


class SalaChat(MediadorChat):
    """Mediador concreto."""

    def __init__(self) -> None:
        self._usuarios: list[Usuario] = []

    def registrar(self, usuario: "Usuario") -> None:
        self._usuarios.append(usuario)
        usuario.sala = self

    def enviar_mensaje(self, mensaje: str, emisor: "Usuario") -> None:
        for usuario in self._usuarios:
            if usuario is not emisor:
                usuario.recibir(mensaje, emisor.nombre)


class Usuario:
    """Colega que se comunica a través del mediador."""

    def __init__(self, nombre: str) -> None:
        self.nombre = nombre
        self.sala: MediadorChat | None = None

    def enviar(self, mensaje: str) -> None:
        if self.sala is None:
            print(f"{self.nombre} no está registrado en ninguna sala.")
            return

        print(f"[{self.nombre} envía]: {mensaje}")
        self.sala.enviar_mensaje(mensaje, self)

    def recibir(self, mensaje: str, emisor: str) -> None:
        print(f"  {self.nombre} recibe de {emisor}: {mensaje}")


def main() -> None:
    sala = SalaChat()

    ana = Usuario("Ana")
    luis = Usuario("Luis")
    maria = Usuario("María")

    sala.registrar(ana)
    sala.registrar(luis)
    sala.registrar(maria)

    ana.enviar("Hola equipo, ¿cómo avanzan con el proyecto?")
    print()
    luis.enviar("Ya terminé el módulo de autenticación.")


if __name__ == "__main__":
    main()
