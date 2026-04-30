#*------------------------------------------------------------------------
#* Ingeniería de Software II
#* TP3 - Patrones de Creación
#* Ejercicio 3: Hamburguesa con Builder + Factory Method
#* UADER - FCyT
#* Rodriguez Paula
#*------------------------------------------------------------------------
"""
Patrones utilizados:
  - Builder      → construye la hamburguesa paso a paso
  - Factory      → decide el método de entrega en tiempo de ejecución

Por qué Builder:
  La hamburguesa tiene múltiples partes opcionales (pan, carne, queso,
  vegetales, salsa). Builder permite armarla de forma legible y flexible
  sin un constructor con demasiados parámetros.

Por qué Factory Method:
  El método de entrega (mostrador, retiro, delivery) varía según el
  pedido. Factory centraliza esa decisión y desacopla al cliente de
  las clases concretas de entrega.
"""

from abc import ABC, abstractmethod


# =============================================================
# PRODUCTO — Hamburguesa
# =============================================================

class Hamburguesa:
    """Objeto complejo construido por el Builder."""

    def __init__(self):
        self.pan       = None
        self.carne     = None
        self.queso     = None
        self.vegetales = []
        self.salsa     = None

    def __str__(self):
        extras = []
        if self.queso:
            extras.append(self.queso)
        extras.extend(self.vegetales)
        if self.salsa:
            extras.append(self.salsa)
        detalle = ", ".join(extras) if extras else "sin extras"
        return f"Hamburguesa [{self.pan} | {self.carne} | {detalle}]"


# =============================================================
# BUILDER ABSTRACTO
# =============================================================

class BuilderHamburguesa(ABC):

    def __init__(self):
        self.reset()

    def reset(self):
        self._hamburguesa = Hamburguesa()

    def obtener_resultado(self) -> Hamburguesa:
        resultado = self._hamburguesa
        self.reset()          # permite reutilizar el builder
        return resultado

    @abstractmethod
    def agregar_pan(self): pass

    @abstractmethod
    def agregar_carne(self): pass

    @abstractmethod
    def agregar_queso(self): pass

    @abstractmethod
    def agregar_vegetales(self): pass

    @abstractmethod
    def agregar_salsa(self): pass


# =============================================================
# BUILDERS CONCRETOS
# =============================================================

class BuilderHamburguesaClasica(BuilderHamburguesa):
    """Hamburguesa clásica: simple y directa."""

    def agregar_pan(self):
        self._hamburguesa.pan = "pan blanco"
        return self

    def agregar_carne(self):
        self._hamburguesa.carne = "carne vacuna"
        return self

    def agregar_queso(self):
        self._hamburguesa.queso = "queso cheddar"
        return self

    def agregar_vegetales(self):
        self._hamburguesa.vegetales = ["lechuga", "tomate"]
        return self

    def agregar_salsa(self):
        self._hamburguesa.salsa = "ketchup"
        return self


class BuilderHamburguesaGourmet(BuilderHamburguesa):
    """Hamburguesa gourmet: ingredientes premium."""

    def agregar_pan(self):
        self._hamburguesa.pan = "pan brioche"
        return self

    def agregar_carne(self):
        self._hamburguesa.carne = "carne angus 200g"
        return self

    def agregar_queso(self):
        self._hamburguesa.queso = "queso brie"
        return self

    def agregar_vegetales(self):
        self._hamburguesa.vegetales = ["rúcula", "cebolla caramelizada"]
        return self

    def agregar_salsa(self):
        self._hamburguesa.salsa = "salsa BBQ ahumada"
        return self


# =============================================================
# DIRECTOR — controla el orden de construcción
# =============================================================

class Director:
    def __init__(self, builder: BuilderHamburguesa):
        self._builder = builder

    def hacer_hamburguesa_completa(self) -> Hamburguesa:
        self._builder.agregar_pan()
        self._builder.agregar_carne()
        self._builder.agregar_queso()
        self._builder.agregar_vegetales()
        self._builder.agregar_salsa()
        return self._builder.obtener_resultado()

    def hacer_hamburguesa_simple(self) -> Hamburguesa:
        """Solo pan + carne, sin extras."""
        self._builder.agregar_pan()
        self._builder.agregar_carne()
        return self._builder.obtener_resultado()


# =============================================================
# FACTORY METHOD — método de entrega
# =============================================================

class MetodoEntrega(ABC):
    """Producto abstracto del Factory."""

    @abstractmethod
    def entregar(self, hamburguesa: Hamburguesa) -> None:
        pass


class EntregaMostrador(MetodoEntrega):
    def entregar(self, hamburguesa: Hamburguesa) -> None:
        print(f"  [MOSTRADOR]  {hamburguesa} — Lista en el mostrador, pase a retirar.")


class EntregaRetiro(MetodoEntrega):
    def entregar(self, hamburguesa: Hamburguesa) -> None:
        print(f"  [RETIRO]     {hamburguesa} — El cliente retira en caja.")


class EntregaDelivery(MetodoEntrega):
    def entregar(self, hamburguesa: Hamburguesa) -> None:
        print(f"  [DELIVERY]   {hamburguesa} — En camino al domicilio del cliente.")


class EntregaFactory:
    """
    Factory que decide qué clase de entrega instanciar.
    El cliente solo pasa un string; no conoce las clases concretas.
    """
    _mapa = {
        "mostrador" : EntregaMostrador,
        "retiro"    : EntregaRetiro,
        "delivery"  : EntregaDelivery,
    }

    @staticmethod
    def crear(tipo: str) -> MetodoEntrega:
        clase = EntregaFactory._mapa.get(tipo.strip().lower())
        if not clase:
            raise ValueError(
                f"Método de entrega desconocido: '{tipo}'. "
                f"Opciones: {list(EntregaFactory._mapa.keys())}"
            )
        return clase()


# =============================================================
# main
# =============================================================

def main():
    print("=" * 58)
    print("  Ejercicio 3 — Builder + Factory: Hamburguesa")
    print("=" * 58)

    # ── Builder: armar hamburgesas ─────────────────────────
    director_clasica = Director(BuilderHamburguesaClasica())
    director_gourmet = Director(BuilderHamburguesaGourmet())

    clasica_completa = director_clasica.hacer_hamburguesa_completa()
    clasica_simple   = director_clasica.hacer_hamburguesa_simple()
    gourmet_completa = director_gourmet.hacer_hamburguesa_completa()

    # ── Factory: elegir método de entrega ──────────────────
    print("\n--- Pedidos del día ---\n")

    pedidos = [
        (clasica_completa, "mostrador"),
        (clasica_simple,   "retiro"),
        (gourmet_completa, "delivery"),
    ]

    for hamburguesa, metodo in pedidos:
        entrega = EntregaFactory.crear(metodo)
        entrega.entregar(hamburguesa)

    # ── Manejo de entrega desconocida ──────────────────────
    print("\n--- Manejo de método de entrega inválido ---")
    try:
        EntregaFactory.crear("dron")
    except ValueError as e:
        print(f"  Error capturado: {e}")


if __name__ == "__main__":
    main()