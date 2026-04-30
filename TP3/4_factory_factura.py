#*------------------------------------------------------------------------
#* Ingeniería de Software II
#* TP3 - Patrones de Creación
#* Ejercicio 4: Factura con Factory Method
#* UADER - FCyT
#* Rodriguez Paula
#*------------------------------------------------------------------------
"""
Patrón utilizado: Factory Method

Por qué Factory Method:
  La factura varía según la condición impositiva del cliente
  (Responsable Inscripto, No Inscripto, Exento). Cada condición
  produce un tipo distinto de factura con su propio comportamiento
  (tipo de comprobante, tratamiento del IVA).
  Factory Method centraliza esa decisión: el cliente pasa el
  importe y la condición, y la fábrica devuelve el objeto correcto
  sin que el código cliente conozca las clases concretas.

Por qué NO Builder:
  La factura no tiene partes opcionales que se ensamblen paso a paso.
  Simplemente existe un importe y una condición → eso determina la clase.
"""

from abc import ABC, abstractmethod


# =============================================================
# PRODUCTO ABSTRACTO
# =============================================================

class Factura(ABC):
    """Interfaz común para todos los tipos de factura."""

    def __init__(self, importe: float):
        if importe < 0:
            raise ValueError(f"El importe no puede ser negativo: {importe}")
        self._importe = importe

    @property
    @abstractmethod
    def tipo(self) -> str:
        """Letra del comprobante: A, B o C."""
        pass

    @property
    @abstractmethod
    def condicion_cliente(self) -> str:
        pass

    @abstractmethod
    def calcular_total(self) -> float:
        """Calcula el total según el tratamiento impositivo."""
        pass

    def imprimir(self) -> None:
        print(f"    FACTURA  {self.tipo:<31}")
        print(f"    Condición cliente: {self.condicion_cliente:<20}")
        print(f"    Importe base:      $ {self._importe:>8.2f}")
        print(f"    Total a pagar:     $ {self.calcular_total():>8.2f}")
        


# =============================================================
# PRODUCTOS CONCRETOS
# =============================================================

class FacturaA(Factura):
    """
    Factura A — cliente Responsable Inscripto.
    El IVA se discrimina: se muestra por separado en la factura.
    Total = base + IVA 21%.
    """
    TASA_IVA = 0.21

    @property
    def tipo(self) -> str:
        return "A"

    @property
    def condicion_cliente(self) -> str:
        return "IVA Responsable Inscripto"

    def calcular_total(self) -> float:
        return round(self._importe * (1 + self.TASA_IVA), 2)

    def imprimir(self) -> None:
        iva = round(self._importe * self.TASA_IVA, 2)
        
        print(f"   FACTURA  {self.tipo:<31}")
        print(f"   Condición: {self.condicion_cliente:<29}")
        print(f"   Neto gravado:$ {self._importe:>8.2f}")
        print(f"   IVA (21%): $ {iva:>8.2f}")
        print(f"   Total a pagar:$ {self.calcular_total():>8.2f}")
      


class FacturaB(Factura):
    """
    Factura B — cliente IVA No Inscripto / Consumidor Final.
    El IVA está incluido en el precio (no se discrimina).
    Total = base (IVA ya incluido).
    """
    @property
    def tipo(self) -> str:
        return "B"

    @property
    def condicion_cliente(self) -> str:
        return "IVA No Inscripto"

    def calcular_total(self) -> float:
        return round(self._importe, 2)


class FacturaC(Factura):
    """
    Factura C — cliente IVA Exento / Monotributista.
    Sin IVA. Total = base imponible sin modificaciones.
    """
    @property
    def tipo(self) -> str:
        return "C"

    @property
    def condicion_cliente(self) -> str:
        return "IVA Exento"

    def calcular_total(self) -> float:
        return round(self._importe, 2)


# =============================================================
# FACTORY METHOD
# =============================================================

class FacturaFactory:
    """
    Fábrica que crea el tipo correcto de Factura
    según la condición impositiva del cliente.
    """

    _mapa = {
        "responsable" : FacturaA,
        "no inscripto": FacturaB,
        "exento"      : FacturaC,
    }

    @staticmethod
    def crear(condicion: str, importe: float) -> Factura:
        """
        Args:
            condicion: 'responsable', 'no inscripto' o 'exento'
            importe:   base imponible de la factura

        Returns:
            Instancia concreta de Factura según la condición.
        """
        clase = FacturaFactory._mapa.get(condicion.strip().lower())
        if not clase:
            raise ValueError(
                f"Condición impositiva desconocida: '{condicion}'. "
                f"Opciones: {list(FacturaFactory._mapa.keys())}"
            )
        return clase(importe)


# =============================================================
# main
# =============================================================

def main():
    print("=" * 54)
    print("  Ejercicio 4 — Factory Method: Factura")
    print("=" * 54)

    pedidos = [
        ("responsable",  10000.00),
        ("no inscripto",  5500.50),
        ("exento",        3200.00),
    ]

    for condicion, importe in pedidos:
        print(f"\n  → Emitiendo factura para cliente '{condicion}', base $ {importe:.2f}:")
        factura = FacturaFactory.crear(condicion, importe)
        factura.imprimir()

    # Manejo de condición inválida
    print("\n--- Manejo de condición impositiva inválida ---")
    try:
        FacturaFactory.crear("monotributo", 1000)
    except ValueError as e:
        print(f"  Error capturado: {e}")


if __name__ == "__main__":
    main()