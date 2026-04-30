#*------------------------------------------------------------------------
#* Ingeniería de Software II
#* TP3 - Patrones de Creación
#* Ejercicio 2: Calculadora de Impuestos con Singleton
#* UADER - FCyT
#* Rodriguez Paula
#*------------------------------------------------------------------------

from threading import Lock


class CalculadorImpuestos:
    """
    Singleton para el cálculo de impuestos.
    Todas las clases del sistema comparten esta única instancia.

    Impuestos aplicados sobre la base imponible:
        - IVA:                      21 %
        - IIBB:                      5 %
        - Contribuciones municipales: 1,2 %
        - Total:                    27,2 %
    """

    _instancia = None
    _lock = Lock()

    # Tasas como constantes de clase
    TASA_IVA          = 0.21
    TASA_IIBB         = 0.05
    TASA_MUNICIPALES  = 0.012

    def __new__(cls):
        if cls._instancia is None:
            with cls._lock:
                if cls._instancia is None:
                    cls._instancia = super().__new__(cls)
        return cls._instancia

    def __init__(self):
        if not hasattr(self, "_inicializado"):
            self._inicializado = True

    # ------------------------------------------------------------------
    # Métodos de cálculo
    # ------------------------------------------------------------------

    def calcular_iva(self, base: float) -> float:
        return round(base * self.TASA_IVA, 2)

    def calcular_iibb(self, base: float) -> float:
        return round(base * self.TASA_IIBB, 2)

    def calcular_municipales(self, base: float) -> float:
        return round(base * self.TASA_MUNICIPALES, 2)

    def calcular_total(self, base: float) -> dict:
        """
        Recibe la base imponible y retorna un dict con el detalle
        de cada impuesto y el total a pagar.
        """
        if base < 0:
            raise ValueError(f"La base imponible no puede ser negativa: {base}")

        iva         = self.calcular_iva(base)
        iibb        = self.calcular_iibb(base)
        municipales = self.calcular_municipales(base)
        total       = round(iva + iibb + municipales, 2)

        return {
            "base_imponible"       : round(base, 2),
            "iva_21"               : iva,
            "iibb_5"               : iibb,
            "contribuciones_1_2"   : municipales,
            "total_impuestos"      : total,
            "importe_final"        : round(base + total, 2),
        }

    def imprimir_liquidacion(self, base: float) -> None:
        """Imprime un resumen legible de la liquidación de impuestos."""
        d = self.calcular_total(base)
        print(f"  Base imponible         : $ {d['base_imponible']:>10.2f}")
        print(f"  IVA          (21 %)    : $ {d['iva_21']:>10.2f}")
        print(f"  IIBB         ( 5 %)    : $ {d['iibb_5']:>10.2f}")
        print(f"  Municipales  ( 1.2%)   : $ {d['contribuciones_1_2']:>10.2f}")
        print(f"  {'─'*30}")
        print(f"  Total impuestos        : $ {d['total_impuestos']:>10.2f}")
        print(f"  Importe final          : $ {d['importe_final']:>10.2f}")


# =============================================================
# Clases que consumen el singleton
# =============================================================

class ModuloVentas:
    """Usa el calculador para liquidar impuestos de una venta."""

    def __init__(self):
        self.impuestos = CalculadorImpuestos()

    def procesar_venta(self, descripcion: str, base: float) -> None:
        print(f"\n  [Ventas] {descripcion}")
        self.impuestos.imprimir_liquidacion(base)


class ModuloContabilidad:
    """Usa el calculador para registrar impuestos en la contabilidad."""

    def __init__(self):
        self.impuestos = CalculadorImpuestos()

    def registrar(self, concepto: str, base: float) -> None:
        resultado = self.impuestos.calcular_total(base)
        print(f"\n  [Contabilidad] {concepto}")
        print(f"  → Total impuestos a registrar: $ {resultado['total_impuestos']:.2f}")
        print(f"  → Importe final al cliente:    $ {resultado['importe_final']:.2f}")


# =============================================================
# main
# =============================================================

def main():
    print("=" * 52)
    print("  Ejercicio 2 — Singleton: CalculadorImpuestos")
    print("=" * 52)

    # Verificación de unicidad
    inst1 = CalculadorImpuestos()
    inst2 = CalculadorImpuestos()
    print(f"\n¿inst1 e inst2 son la misma instancia? {inst1 is inst2}")

    # Cálculo directo
    print("\n--- Liquidación directa (base $ 1000) ---")
    calc = CalculadorImpuestos()
    calc.imprimir_liquidacion(1000)

    # Uso desde distintos módulos
    ventas       = ModuloVentas()
    contabilidad = ModuloContabilidad()

    ventas.procesar_venta("Venta de mercadería", 5000)
    contabilidad.registrar("Servicio de consultoría", 12000)

    # Verificar instancia compartida entre módulos
    print(f"\n--- Verificación instancia compartida ---")
    print(f"  ModuloVentas.impuestos is ModuloContabilidad.impuestos → "
          f"{ventas.impuestos is contabilidad.impuestos}")

    # Manejo de error
    print("\n--- Manejo de entrada inválida ---")
    try:
        calc.calcular_total(-500)
    except ValueError as e:
        print(f"  Error capturado: {e}")


if __name__ == "__main__":
    main()