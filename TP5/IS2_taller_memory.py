#*------------------------------------------------------------------------
#* Ingeniería de Software II
#* Patrones de Comportamiento
#* Memento - TP5 Punto 5
#* Modificación de IS2_taller_memory.py
#* UADER - Ingeniería de Software II
#* Rodriguez Paula
#*------------------------------------------------------------------------

import os
import platform


# =============================================================================
# CLASE MEMENTO: sin cambios respecto al original
# =============================================================================

class Memento:
    """
    Memento.
    Guarda una instantánea del estado del escritor (nombre de archivo + contenido).
    No puede ser modificado desde afuera; solo el Originator lo usa.
    """

    def __init__(self, file, content):
        self.file    = file
        self.content = content


# =============================================================================
# ORIGINATOR: sin cambios respecto al original
# =============================================================================

class FileWriterUtility:
    """
    Originator.
    Objeto cuyo estado se quiere preservar.
    Sabe crear y restaurar sus propios mementos.
    """

    def __init__(self, file):
        self.file    = file
        self.content = ""

    def write(self, string):
        self.content += string

    def save(self):
        """Crea y devuelve un memento con el estado actual."""
        return Memento(self.file, self.content)

    def undo(self, memento):
        """Restaura el estado a partir de un memento."""
        self.file    = memento.file
        self.content = memento.content


# =============================================================================
# CARETAKER: modificado para soportar hasta 4 estados
# =============================================================================

class FileWriterCaretaker:
    """
    Caretaker extendido.
    Almacena hasta 4 mementos en una lista ordenada del más antiguo al más reciente.
    undo(writer, n) recupera el estado según el índice:
      n=0 → el más reciente guardado
      n=1 → el anterior a ese
      n=2 → dos posiciones atrás
      n=3 → el más antiguo disponible
    Si el índice pedido no existe, informa y no modifica el estado.
    """

    MAX_ESTADOS = 4

    def __init__(self):
        # Lista de mementos: el último elemento es el más reciente
        self._historial: list[Memento] = []

    def save(self, writer: FileWriterUtility) -> None:
        """
        Guarda el estado actual del writer.
        Si ya hay 4 estados guardados, descarta el más antiguo
        para hacer lugar al nuevo (ventana deslizante de 4).
        """
        if len(self._historial) >= self.MAX_ESTADOS:
            self._historial.pop(0)   # descarta el más antiguo
        self._historial.append(writer.save())
        print(f"[Caretaker] Estado guardado. Historial: {len(self._historial)} estado(s).")

    def undo(self, writer: FileWriterUtility, n: int = 0) -> None:
        """
        Restaura el estado según el índice n:
          n=0 → inmediato anterior (el más reciente del historial)
          n=1 → el anterior a ese
          n=2 → dos posiciones atrás
          n=3 → el más antiguo disponible
        El historial NO se modifica: se puede hacer undo varias veces
        con distintos índices sin perder los estados guardados.
        """
        if not self._historial:
            print("[Caretaker] No hay estados guardados.")
            return

        # El índice 0 corresponde al último elemento de la lista
        indice_real = len(self._historial) - 1 - n

        if indice_real < 0:
            print(f"[Caretaker] No existe un estado en la posición {n}. "
                  f"Solo hay {len(self._historial)} estado(s) guardado(s).")
            return

        writer.undo(self._historial[indice_real])
        print(f"[Caretaker] Estado restaurado desde posición {n}.")


# =============================================================================
# Punto de entrada
# =============================================================================

if __name__ == "__main__":
    os.system("cls" if platform.system() == "Windows" else "clear")

    caretaker = FileWriterCaretaker()
    writer    = FileWriterUtility("archivo.txt")

    # Se graban 4 versiones distintas del contenido
    print("=== Grabando estados ===\n")

    writer.write("Línea 1: Clase de IS2 en UADER\n")
    caretaker.save(writer)
    print(f"Contenido actual:\n{writer.content}")

    writer.write("Línea 2: Patrones de comportamiento\n")
    caretaker.save(writer)
    print(f"Contenido actual:\n{writer.content}")

    writer.write("Línea 3: Memento pattern\n")
    caretaker.save(writer)
    print(f"Contenido actual:\n{writer.content}")

    writer.write("Línea 4: Modificación del taller\n")
    caretaker.save(writer)
    print(f"Contenido actual:\n{writer.content}")

    # Recuperación por índice
    print("=== Recuperando estados por índice ===\n")

    print("-- undo(0): inmediato anterior --")
    caretaker.undo(writer, 0)
    print(f"Contenido:\n{writer.content}")

    print("-- undo(1): dos versiones atrás --")
    caretaker.undo(writer, 1)
    print(f"Contenido:\n{writer.content}")

    print("-- undo(2): tres versiones atrás --")
    caretaker.undo(writer, 2)
    print(f"Contenido:\n{writer.content}")

    print("-- undo(3): el más antiguo --")
    caretaker.undo(writer, 3)
    print(f"Contenido:\n{writer.content}")

    print("-- undo(4): índice inexistente --")
    caretaker.undo(writer, 4)