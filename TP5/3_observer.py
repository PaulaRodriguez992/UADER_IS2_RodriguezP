#*------------------------------------------------------------------------
#* Ingeniería de Software II
#* Patrones de Comportamiento
#* Observer - TP5 Punto 3
#* UADER - Ingeniería de Software II
#* Rodriguez Paula
#*------------------------------------------------------------------------

import os
import platform
from abc import ABC, abstractmethod


class ObservadorID(ABC):
    """
    Interfaz común para todos los observadores.
    Cada uno tiene un ID propio de 4 caracteres y reacciona
    solo cuando el ID emitido coincide con el suyo.
    """

    def __init__(self, id_propio: str) -> None:
        self.id_propio = id_propio

    @abstractmethod
    def actualizar(self, id_emitido: str) -> None:
        pass


class EmisorID:
    """
    Sujeto observado.
    Emite IDs de 4 caracteres y notifica a todos los subscriptos.
    Cada observador decide por sí mismo si le corresponde reaccionar.
    """

    def __init__(self) -> None:
        self._observadores: list[ObservadorID] = []

    def subscribir(self, observador: ObservadorID) -> None:
        self._observadores.append(observador)

    def desubscribir(self, observador: ObservadorID) -> None:
        self._observadores.remove(observador)

    def emitir(self, id_emitido: str) -> None:
        """Emite un ID y notifica a todos los subscriptos."""
        print(f"\n[Emisor] ID emitido: {id_emitido}")
        for observador in self._observadores:
            observador.actualizar(id_emitido)


class ClaseALFA(ObservadorID):
    """Observador concreto con ID 'ALFA'."""

    def __init__(self) -> None:
        super().__init__("ALFA")

    def actualizar(self, id_emitido: str) -> None:
        if id_emitido == self.id_propio:
            print(f"  [ClaseALFA] ¡Coincidencia! ID '{id_emitido}' es el mío.")


class ClaseBETA(ObservadorID):
    """Observador concreto con ID 'BETA'."""

    def __init__(self) -> None:
        super().__init__("BETA")

    def actualizar(self, id_emitido: str) -> None:
        if id_emitido == self.id_propio:
            print(f"  [ClaseBETA] ¡Coincidencia! ID '{id_emitido}' es el mío.")


class ClaseGAMA(ObservadorID):
    """Observador concreto con ID 'GAMA'."""

    def __init__(self) -> None:
        super().__init__("GAMA")

    def actualizar(self, id_emitido: str) -> None:
        if id_emitido == self.id_propio:
            print(f"  [ClaseGAMA] ¡Coincidencia! ID '{id_emitido}' es el mío.")


class ClaseDELT(ObservadorID):
    """Observador concreto con ID 'DELT'."""

    def __init__(self) -> None:
        super().__init__("DELT")

    def actualizar(self, id_emitido: str) -> None:
        if id_emitido == self.id_propio:
            print(f"  [ClaseDELT] ¡Coincidencia! ID '{id_emitido}' es el mío.")


if __name__ == "__main__":
    os.system("cls" if platform.system() == "Windows" else "clear")

    # Se instancia el sujeto y los 4 observadores
    emisor = EmisorID()

    emisor.subscribir(ClaseALFA())
    emisor.subscribir(ClaseBETA())
    emisor.subscribir(ClaseGAMA())
    emisor.subscribir(ClaseDELT())

    # 8 IDs emitidos: los primeros 4 coinciden con cada clase,
    # los últimos 4 no tienen clase subscripta → nadie responde
    ids_a_emitir = ["ALFA", "BETA", "GAMA", "DELT", "ZETA", "LAMB", "OMEG", "KAPA"]

    print("=== Emitiendo 8 IDs ===")
    for id_emitido in ids_a_emitir:
        emisor.emitir(id_emitido)