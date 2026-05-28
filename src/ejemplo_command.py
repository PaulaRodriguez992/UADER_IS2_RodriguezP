# Ejemplo práctico de aplicación de patrón command
#*------------------------------------------------------------------------
#* Ingeniería de Software II
#* Patrones de Creación
#* Command
#* UADER - Ingeniería de Software II
#* Dr. Pedro E. Colla
#*------------------------------------------------------------------------
"""
Command es útil cuando se deben convertir acciones en objetos.

Casos típicos:
	deshacer / rehacer
	colas de tareas
	acciones de menú o botones
	macros
	logging de operaciones
	transacciones
	procesamiento asincrónico
	planificación de trabajos


Command separa quién solicita una acción de quién la ejecuta.
En lugar de ejecutar una acción directamente, la empaquetamos como un objeto que puede
 ejecutarse, guardarse, repetirse o deshacerse.
"""
from abc import ABC, abstractmethod


class EditorTexto:
    """Receiver: objeto que realiza el trabajo real."""

    def __init__(self) -> None:
        self.contenido = ""

    def escribir(self, texto: str) -> None:
        self.contenido += texto

    def borrar_ultimos(self, cantidad: int) -> str:
        texto_borrado = self.contenido[-cantidad:]
        self.contenido = self.contenido[:-cantidad]
        return texto_borrado

    def mostrar(self) -> None:
        print(f"Contenido actual: '{self.contenido}'")


class Comando(ABC):
    """Interfaz común para todos los comandos."""

    @abstractmethod
    def ejecutar(self) -> None:
        pass

    @abstractmethod
    def deshacer(self) -> None:
        pass


class ComandoEscribir(Comando):
    """Command concreto: escribir texto."""

    def __init__(self, editor: EditorTexto, texto: str) -> None:
        self.editor = editor
        self.texto = texto

    def ejecutar(self) -> None:
        self.editor.escribir(self.texto)

    def deshacer(self) -> None:
        self.editor.borrar_ultimos(len(self.texto))


class ComandoBorrar(Comando):
    """Command concreto: borrar caracteres."""

    def __init__(self, editor: EditorTexto, cantidad: int) -> None:
        self.editor = editor
        self.cantidad = cantidad
        self.texto_borrado = ""

    def ejecutar(self) -> None:
        self.texto_borrado = self.editor.borrar_ultimos(self.cantidad)

    def deshacer(self) -> None:
        self.editor.escribir(self.texto_borrado)


class HistorialComandos:
    """Invoker: ejecuta comandos y conserva historial para deshacer."""

    def __init__(self) -> None:
        self.historial: list[Comando] = []

    def ejecutar_comando(self, comando: Comando) -> None:
        comando.ejecutar()
        self.historial.append(comando)

    def deshacer_ultimo(self) -> None:
        if not self.historial:
            print("No hay comandos para deshacer.")
            return

        comando = self.historial.pop()
        comando.deshacer()


def main() -> None:
    editor = EditorTexto()
    historial = HistorialComandos()

    historial.ejecutar_comando(ComandoEscribir(editor, "Hola "))
    historial.ejecutar_comando(ComandoEscribir(editor, "mundo"))
    editor.mostrar()

    historial.ejecutar_comando(ComandoBorrar(editor, 5))
    editor.mostrar()

    historial.deshacer_ultimo()
    editor.mostrar()

    historial.deshacer_ultimo()
    editor.mostrar()


if __name__ == "__main__":
    main()
