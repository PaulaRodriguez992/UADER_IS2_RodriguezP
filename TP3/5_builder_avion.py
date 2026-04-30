#*------------------------------------------------------------------------
#* Ingeniería de Software II
#* TP3 - Patrones de Creación
#* Ejercicio 5: Builder para Aviones
#* UADER - FCyT
#* Rodriguez Paula
#*------------------------------------------------------------------------
"""
Patrón utilizado: Builder

Por qué Builder:
  Extensión directa del ejemplo del taller (BuilderComputadora).
  
  Un avión se construye paso a paso con partes bien definidas:
  body, turbinas (x2), alas (x2) y tren de aterrizaje.
  El Director controla el orden de ensamble sin conocer los
  detalles concretos de cada variante de avión.

Estructura (igual que el ejemplo):
  Avion              ← Producto
  BuilderAvion       ← Builder abstracto
  BuilderAvionComercial / BuilderAvionCarga  ← Builders concretos
  Director           ← Controla el orden de construcción
"""

from __future__ import annotations
from abc import ABC, abstractmethod


# =============================================================
# PRODUCTO
# =============================================================

class Avion:
    """Producto complejo ensamblado por el Builder."""

    def __init__(self):
        self.partes: list[str] = []

    def agregar(self, parte: str) -> None:
        self.partes.append(parte)

    def mostrar(self) -> str:
        return "Avión ensamblado con:\n  - " + "\n  - ".join(self.partes)


# =============================================================
# BUILDER ABSTRACTO
# =============================================================

class BuilderAvion(ABC):
    """Define los pasos de construcción de un avión."""

    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self._avion = Avion()

    def obtener_resultado(self) -> Avion:
        avion = self._avion
        self.reset()          # listo para reutilizar
        return avion

    @abstractmethod
    def construir_body(self) -> None:
        pass

    @abstractmethod
    def construir_turbinas(self) -> None:
        """Siempre 2 turbinas."""
        pass

    @abstractmethod
    def construir_alas(self) -> None:
        """Siempre 2 alas."""
        pass

    @abstractmethod
    def construir_tren_aterrizaje(self) -> None:
        pass


# =============================================================
# BUILDERS CONCRETOS
# =============================================================

class BuilderAvionComercial(BuilderAvion):
    """Avión de pasajeros — configuración estándar de aerolínea."""

    def construir_body(self) -> None:
        self._avion.agregar("Body: fuselaje ancho para pasajeros (wide-body)")

    def construir_turbinas(self) -> None:
        self._avion.agregar("Turbina 1: turbofán de alto bypass")
        self._avion.agregar("Turbina 2: turbofán de alto bypass")

    def construir_alas(self) -> None:
        self._avion.agregar("Ala 1: ala en flecha con winglets")
        self._avion.agregar("Ala 2: ala en flecha con winglets")

    def construir_tren_aterrizaje(self) -> None:
        self._avion.agregar("Tren de aterrizaje: triciclo retráctil con 6 ruedas")


class BuilderAvionCarga(BuilderAvion):
    """Avión de carga — mayor capacidad de bodega, estructura reforzada."""

    def construir_body(self) -> None:
        self._avion.agregar("Body: fuselaje reforzado con puerta de carga frontal")

    def construir_turbinas(self) -> None:
        self._avion.agregar("Turbina 1: turbofán de alta potencia para carga")
        self._avion.agregar("Turbina 2: turbofán de alta potencia para carga")

    def construir_alas(self) -> None:
        self._avion.agregar("Ala 1: ala de alta sustentación para despegue cargado")
        self._avion.agregar("Ala 2: ala de alta sustentación para despegue cargado")

    def construir_tren_aterrizaje(self) -> None:
        self._avion.agregar("Tren de aterrizaje: reforzado con 10 ruedas para mayor peso")


class BuilderAvionMilitar(BuilderAvion):
    """Avión de combate — ligero, veloz, furtivo."""

    def construir_body(self) -> None:
        self._avion.agregar("Body: fuselaje furtivo con geometría de baja observabilidad")

    def construir_turbinas(self) -> None:
        self._avion.agregar("Turbina 1: turbofán con postquemador supersónico")
        self._avion.agregar("Turbina 2: turbofán con postquemador supersónico")

    def construir_alas(self) -> None:
        self._avion.agregar("Ala 1: ala delta de geometría variable")
        self._avion.agregar("Ala 2: ala delta de geometría variable")

    def construir_tren_aterrizaje(self) -> None:
        self._avion.agregar("Tren de aterrizaje: compacto retráctil de 3 ruedas")


# =============================================================
# DIRECTOR
# =============================================================

class Director:
    """
    Controla el orden de ensamble del avión.
    No conoce detalles concretos de ninguna variante.
    Orden siempre: body → turbinas → alas → tren de aterrizaje
    """

    def __init__(self, builder: BuilderAvion) -> None:
        self._builder = builder

    def cambiar_builder(self, builder: BuilderAvion) -> None:
        self._builder = builder

    def construir_avion_completo(self) -> None:
        """Ensambla todas las partes en el orden correcto."""
        self._builder.construir_body()
        self._builder.construir_turbinas()
        self._builder.construir_alas()
        self._builder.construir_tren_aterrizaje()

    def construir_avion_sin_tren(self) -> None:
        """Variante: sin tren de aterrizaje (ej: prototipo en pruebas)."""
        self._builder.construir_body()
        self._builder.construir_turbinas()
        self._builder.construir_alas()


# =============================================================
# main
# =============================================================

def main():
    print("=" * 55)
    print("  Ejercicio 5 — Builder: Construcción de Aviones")
    print("=" * 55)

    # ── Avión Comercial completo ───────────────────────────
    print("\n--- Avión Comercial (completo) ---")
    builder_comercial = BuilderAvionComercial()
    director = Director(builder_comercial)
    director.construir_avion_completo()
    avion_comercial = builder_comercial.obtener_resultado()
    print(avion_comercial.mostrar())

    # ── Avión de Carga completo ────────────────────────────
    print("\n--- Avión de Carga (completo) ---")
    builder_carga = BuilderAvionCarga()
    director.cambiar_builder(builder_carga)
    director.construir_avion_completo()
    avion_carga = builder_carga.obtener_resultado()
    print(avion_carga.mostrar())

    # ── Avión Militar completo ─────────────────────────────
    print("\n--- Avión Militar (completo) ---")
    builder_militar = BuilderAvionMilitar()
    director.cambiar_builder(builder_militar)
    director.construir_avion_completo()
    avion_militar = builder_militar.obtener_resultado()
    print(avion_militar.mostrar())

    # ── Variante: prototipo sin tren de aterrizaje ─────────
    print("\n--- Avión Comercial (prototipo, sin tren de aterrizaje) ---")
    director.cambiar_builder(BuilderAvionComercial())
    director.construir_avion_sin_tren()
    avion_proto = director._builder.obtener_resultado()
    print(avion_proto.mostrar())


if __name__ == "__main__":
    main()