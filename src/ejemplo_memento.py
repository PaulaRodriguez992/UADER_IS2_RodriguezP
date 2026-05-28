# Ejemplo práctico de aplicación de patrón memento
#*------------------------------------------------------------------------
#* Ingeniería de Software II
#* Patrones de Creación
#* Memento
#* UADER - Ingeniería de Software II
#* Dr. Pedro E. Colla
#*------------------------------------------------------------------------
"""
Memento es útil cuando se necesita:

	implementar deshacer/rehacer,
	guardar puntos de restauración,
	conservar snapshots,
	volver a una configuración anterior,
	restaurar el estado de un proceso,
	probar escenarios alternativos sin perder el estado original.

Casos típicos:

	editores de texto,
	editores gráficos,
	videojuegos con partidas guardadas,
	asistentes de configuración,
	simuladores,
	workflows con rollback.

Diferencia con Command
Ambos pueden usarse para deshacer, pero con enfoques distintos.
Command guarda acciones ejecutadas y sabe revertirlas.
Memento guarda estados completos y restaura un estado anterior.


Command deshace operaciones; Memento restaura snapshots.
"""
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Memento:
    """
    Memento.

    Guarda una instantánea del estado interno del editor.
    """
    contenido: str
    fecha: datetime


class EditorTexto:
    """
    Originator.

    Objeto cuyo estado queremos guardar y restaurar.
    """

    def __init__(self) -> None:
        self._contenido = ""

    def escribir(self, texto: str) -> None:
        self._contenido += texto

    def borrar(self, cantidad: int) -> None:
        self._contenido = self._contenido[:-cantidad]

    def guardar_estado(self) -> Memento:
        return Memento(
            contenido=self._contenido,
            fecha=datetime.now(),
        )

    def restaurar_estado(self, memento: Memento) -> None:
        self._contenido = memento.contenido

    def mostrar(self) -> None:
        print(f"Contenido actual: '{self._contenido}'")


class HistorialEditor:
    """
    Caretaker.

    Guarda los mementos, pero no modifica ni interpreta su contenido.
    """

    def __init__(self) -> None:
        self._historial: list[Memento] = []

    def guardar(self, editor: EditorTexto) -> None:
        self._historial.append(editor.guardar_estado())

    def deshacer(self, editor: EditorTexto) -> None:
        if not self._historial:
            print("No hay estados anteriores para restaurar.")
            return

        memento = self._historial.pop()
        editor.restaurar_estado(memento)


def main() -> None:
    editor = EditorTexto()
    historial = HistorialEditor()

    historial.guardar(editor)
    editor.escribir("Hola ")

    historial.guardar(editor)
    editor.escribir("mundo")

    historial.guardar(editor)
    editor.escribir("!")

    editor.mostrar()

    print("Deshaciendo último cambio...")
    historial.deshacer(editor)
    editor.mostrar()

    print("Deshaciendo otro cambio...")
    historial.deshacer(editor)
    editor.mostrar()

    print("Deshaciendo otro cambio...")
    historial.deshacer(editor)
    editor.mostrar()


if __name__ == "__main__":
    main()
