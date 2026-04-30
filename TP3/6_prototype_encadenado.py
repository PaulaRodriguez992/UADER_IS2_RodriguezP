#*------------------------------------------------------------------------
#* Ingeniería de Software II
#* TP3 - Patrones de Creación
#* Ejercicio 6: Prototype encadenado
#* UADER - FCyT
#* Rodriguez Paula
#*------------------------------------------------------------------------
"""
Patrón utilizado: Prototype

Por qué Prototype:
  Permite crear nuevos objetos copiando uno existente sin depender
  de su clase concreta. En este ejercicio se verifica que el patrón
  se propaga: un objeto clonado hereda la capacidad de clonarse,
  generando una cadena de copias totalmente independientes entre sí.

Qué se verifica:
  original → clon1 → clon2
  - Cada nivel puede clonar al siguiente.
  - Las modificaciones en un nivel NO afectan a los demás
    (gracias a deepcopy).
  - Todos comparten la interfaz clone(), independientemente
    de en qué nivel de la cadena se encuentren.
"""

import copy
from abc import ABC, abstractmethod


# =============================================================
# INTERFAZ PROTOTYPE
# =============================================================

class Prototype(ABC):
    """Interfaz que garantiza que todo objeto puede clonarse."""

    @abstractmethod
    def clone(self) -> "Prototype":
        pass


# =============================================================
# CLASE CONCRETA — Expediente
# =============================================================

class Expediente(Prototype):
    """
    Simula un expediente administrativo con datos anidados.
    Los atributos mutables (listas, dicts) son clave para
    demostrar que deepcopy genera copias verdaderamente independientes.
    """

    def __init__(self, numero: str, descripcion: str, metadata: dict):
        self.numero      = numero
        self.descripcion = descripcion
        self.metadata    = metadata    # dict mutable → deepcopy es esencial

    def clone(self) -> "Expediente":
        """Retorna una copia profunda e independiente de este expediente."""
        return copy.deepcopy(self)

    def __str__(self) -> str:
        return (
            f"  Expediente #{self.numero}\n"
            f"    Descripción : {self.descripcion}\n"
            f"    Metadata    : {self.metadata}"
        )


# =============================================================
# VERIFICACIÓN DE INDEPENDENCIA
# =============================================================

def verificar_independencia(nombre_a: str, obj_a, nombre_b: str, obj_b) -> None:
    """Confirma que dos objetos son instancias distintas en memoria."""
    mismo_objeto  = obj_a is obj_b
    mismo_meta    = obj_a.metadata is obj_b.metadata
    print(f"  ¿{nombre_a} is {nombre_b}?             {mismo_objeto}  "
          f"{'Son el mismo objeto!' if mismo_objeto else '✓ instancias distintas'}")
    print(f"  ¿{nombre_a}.metadata is {nombre_b}.metadata?  {mismo_meta}  "
          f"{'Comparten metadata!' if mismo_meta else '✓ metadata independiente'}")


# =============================================================
# main
# =============================================================

def main():
    print("=" * 57)
    print("  Ejercicio 6 — Prototype: Clonación encadenada")
    print("=" * 57)

    # ── Nivel 0: objeto original ───────────────────────────
    original = Expediente(
        numero      = "EXP-001",
        descripcion = "Solicitud de habilitación comercial",
        metadata    = {
            "autor"   : "Rodriguez Paula",
            "version" : 1,
            "tags"    : ["habilitacion", "comercio"]
        }
    )

    print("\n=== NIVEL 0: Original ===")
    print(original)

    # ── Nivel 1: clon generado desde el original ───────────
    clon1 = original.clone()
    clon1.numero        = "EXP-001-A"
    clon1.descripcion   = "Copia para revisión interna"
    clon1.metadata["version"] = 2
    clon1.metadata["tags"].append("revision")

    print("\n=== NIVEL 1: Clon del original ===")
    print(clon1)

    # ── Nivel 2: clon generado desde el clon ──────────────
    # Aquí se verifica lo que pide el ejercicio:
    # el clon también puede generar copias de sí mismo
    clon2 = clon1.clone()
    clon2.numero        = "EXP-001-A-FINAL"
    clon2.descripcion   = "Versión final para archivo"
    clon2.metadata["version"] = 3
    clon2.metadata["tags"].append("archivo")

    print("\n=== NIVEL 2: Clon del clon ===")
    print(clon2)

    # ── Verificar que el original quedó intacto ────────────
    print("\n=== NIVEL 0 después de todas las modificaciones ===")
    print(original)

    # ── Verificaciones de independencia ───────────────────
    print("\n--- Verificación de independencia entre niveles ---")
    verificar_independencia("original", original, "clon1",    clon1)
    print()
    verificar_independencia("clon1",    clon1,    "clon2",    clon2)
    print()
    verificar_independencia("original", original, "clon2",    clon2)

    # ── Resumen de la cadena ───────────────────────────────
    print("\n--- Resumen de la cadena de clonación ---")
    for obj, etiqueta in [(original, "original"),
                          (clon1,    "clon1   "),
                          (clon2,    "clon2   ")]:
        print(f"  {etiqueta}  →  #{obj.numero}  "
              f"v{obj.metadata['version']}  "
              f"tags={obj.metadata['tags']}")

    # ── Confirmar que clone() está disponible en todos ─────
    print("\n--- Todos los niveles tienen clone() disponible ---")
    for obj, nombre in [(original, "original"),
                        (clon1,    "clon1   "),
                        (clon2,    "clon2   ")]:
        tiene = callable(getattr(obj, "clone", None))
        print(f"  {nombre}.clone() disponible: {tiene} ✓")


if __name__ == "__main__":
    main()