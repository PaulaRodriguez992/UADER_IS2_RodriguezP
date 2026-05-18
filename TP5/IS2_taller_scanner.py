#*------------------------------------------------------------------------
#* Ingeniería de Software II
#* Patrones de Comportamiento
#* State - TP5 Punto 4
#* Modificación de IS2_taller_scanner.py
#* UADER - Ingeniería de Software II
#* Rodriguez Paula
#*------------------------------------------------------------------------

import os
import platform


# =============================================================================
# CLASES ORIGINALES (sin modificación)
# =============================================================================

class State:
    """Clase base de estado: define el comportamiento de scan."""

    def scan(self):
        self.pos += 1
        if self.pos == len(self.stations):
            self.pos = 0
        print("Sintonizando... Estación {} {}".format(self.stations[self.pos], self.name))


class AmState(State):
    """Estado AM: barre las estaciones de amplitud modulada."""

    def __init__(self, radio):
        self.radio    = radio
        self.stations = ["1250", "1380", "1510"]
        self.pos      = 0
        self.name     = "AM"

    def toggle_amfm(self):
        print("Cambiando a FM")
        self.radio.state = self.radio.fmstate


class FmState(State):
    """Estado FM: barre las estaciones de frecuencia modulada."""

    def __init__(self, radio):
        self.radio    = radio
        self.stations = ["81.3", "89.1", "103.9"]
        self.pos      = 0
        self.name     = "FM"

    def toggle_amfm(self):
        print("Cambiando a AM")
        self.radio.state = self.radio.amstate


# =============================================================================
# CLASE NUEVA: banco de memorias
# =============================================================================

class MemoriaState:
    """
    Estado de memorias.
    Almacena 4 frecuencias memorizadas (M1-M4), cada una con su banda (AM/FM).
    Al llamar a scan() recorre las memorias en orden circular.
    """

    def __init__(self):
        # Cada memoria es un dict con etiqueta, banda y frecuencia
        # Se definen 2 de AM y 2 de FM para mostrar que pueden mezclarse
        self.memorias = [
            {"etiqueta": "M1", "banda": "AM", "frecuencia": "1250"},
            {"etiqueta": "M2", "banda": "FM", "frecuencia": "103.9"},
            {"etiqueta": "M3", "banda": "AM", "frecuencia": "1510"},
            {"etiqueta": "M4", "banda": "FM", "frecuencia": "89.1"},
        ]
        self.pos = 0

    def scan(self):
        """Recorre las memorias una por una en orden circular."""
        memoria = self.memorias[self.pos]
        print("Memoria {} → {} {}".format(
            memoria["etiqueta"],
            memoria["frecuencia"],
            memoria["banda"]
        ))
        self.pos = (self.pos + 1) % len(self.memorias)

    def scan_todas(self):
        """Recorre las 4 memorias en un solo ciclo."""
        print("--- Barrido de memorias ---")
        for memoria in self.memorias:
            print("  {} → {} {}".format(
                memoria["etiqueta"],
                memoria["frecuencia"],
                memoria["banda"]
            ))
        print("--- Fin de memorias ---")


# =============================================================================
# CLASE RADIO: extendida con soporte de memorias
# =============================================================================

class Radio:
    """
    Radio extendida.
    Mantiene los estados AM y FM originales y agrega
    el banco de memorias M1-M4 como estado independiente.
    """

    def __init__(self):
        self.fmstate  = FmState(self)
        self.amstate  = AmState(self)
        self.memorias = MemoriaState()   # nuevo: banco de memorias

        # Inicialmente en FM (igual que el original)
        self.state = self.fmstate

    def toggle_amfm(self):
        self.state.toggle_amfm()

    def scan(self):
        """Barrido normal de estaciones AM o FM según estado actual."""
        self.state.scan()

    def scan_memorias(self):
        """Barrido de las 4 frecuencias memorizadas."""
        self.memorias.scan_todas()


# =============================================================================
# Punto de entrada
# =============================================================================

if __name__ == "__main__":
    os.system("cls" if platform.system() == "Windows" else "clear")

    print("Crea un objeto radio con memorias M1-M4")
    radio = Radio()

    # Ciclo de acciones: igual al original + scan de memorias en cada ciclo
    # Original: 3 scan FM → toggle → 3 scan AM  (repetido 2 veces)
    # Nuevo:    ídem + scan_memorias al final de cada ciclo
    actions = (
        [radio.scan] * 3
        + [radio.toggle_amfm]
        + [radio.scan] * 3
        + [radio.scan_memorias]   # memorias al final de cada ciclo
    )
    actions *= 2

    print("Recorriendo estaciones y memorias...\n")
    for action in actions:
        action()