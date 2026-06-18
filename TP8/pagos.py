"""
pagos.py
Sistema automatizado de pagos con selección balanceada de cuentas bancarias.
Utiliza el Singleton de getJason.py para obtener los tokens de cada cuenta,
el patrón Chain of Responsibility para rutear pagos automáticamente,
y el patrón Iterator para listar los pagos realizados.
Uso: python3 pagos.py
copyright UADER-FCyT-IS2©2024 todos los derechos reservados
"""

from getJason import classJsonReader


VERSION = "1.2"


class Pago:
    """Representa un pago realizado: número de pedido, token usado y monto."""

    def __init__(self, nro_pedido, token, monto):
        """Inicializa el pago con su número de pedido, token y monto."""
        self.numero = nro_pedido
        self.token = token
        self.monto = monto

    def __str__(self):
        """Devuelve una representación legible del pago."""
        return f"Pedido #{self.numero} | Token: {self.token} | Monto: ${self.monto:.2f}"

    def to_dict(self):
        """Devuelve el pago como diccionario."""
        return {"numero": self.numero, "token": self.token, "monto": self.monto}


class IteradorPagos:
    """Iterador sobre una lista de pagos (patrón Iterator)."""

    def __init__(self, pagos):
        """Recibe la lista de pagos y comienza desde el índice 0."""
        self._pagos = pagos
        self._indice = 0

    def __iter__(self):
        """Devuelve el propio iterador."""
        return self

    def __next__(self):
        """Devuelve el siguiente pago o detiene la iteración."""
        if self._indice >= len(self._pagos):
            raise StopIteration
        pago = self._pagos[self._indice]
        self._indice += 1
        return pago


class CuentaBancaria:
    """
    Eslabón de la cadena de responsabilidad.
    Representa una cuenta bancaria con un token, saldo disponible
    y una referencia al siguiente eslabón de la cadena.
    """

    def __init__(self, token, saldo_inicial):
        """Inicializa la cuenta con su token, saldo y sin sucesor."""
        self.token = token
        self.saldo = saldo_inicial
        self._siguiente = None
        reader = classJsonReader()
        self.clave = reader.compute(self.token)

    def set_siguiente(self, cuenta):
        """Establece el siguiente eslabón en la cadena."""
        self._siguiente = cuenta
        return cuenta

    def procesar(self, numero_pedido, monto):
        """
        Intenta procesar el pago en esta cuenta.
        Si tiene saldo suficiente, lo descuenta y devuelve un objeto Pago.
        Si no, delega al siguiente eslabón. Si no hay siguiente, devuelve None.
        """
        if self.saldo >= monto:
            self.saldo -= monto
            return Pago(numero_pedido, self.token, monto)
        if self._siguiente is not None:
            return self._siguiente.procesar(numero_pedido, monto)
        return None


class GestorPagos:
    """
    Gestiona la cadena de cuentas y los pagos realizados.
    Alterna el punto de entrada de la cadena para lograr un ruteo balanceado.
    """

    def __init__(self):
        """Inicializa las dos cuentas, construye la cadena y prepara el historial."""
        self._cuenta1 = CuentaBancaria("token1", 1000.0)
        self._cuenta2 = CuentaBancaria("token2", 2000.0)

        # Cadena directa: cuenta1 -> cuenta2
        self._cuenta1.set_siguiente(self._cuenta2)

        # Cadena inversa: cuenta2 -> cuenta1
        self._cuenta2_inv = CuentaBancaria("token2", 0.0)
        self._cuenta1_inv = CuentaBancaria("token1", 0.0)

        self._historial = []
        self._turno = 0  # 0 = empieza por cuenta1, 1 = empieza por cuenta2

    def solicitar_pago(self, numero_pedido, monto):
        """
        Recibe una solicitud de pago y la rutea automáticamente.
        Alterna el orden de la cadena para balancear entre cuentas.
        Imprime el resultado del pedido.
        """
        if self._turno == 0:
            pago = self._cuenta1.procesar(numero_pedido, monto)
        else:
            pago = self._cuenta2.procesar(numero_pedido, monto)

        self._turno = 1 - self._turno  # alternar turno

        if pago is not None:
            self._historial.append(pago)
            print(f"PAGO REALIZADO  -> {pago}")
        else:
            print(f"Pedido #{numero_pedido} | RECHAZADO: sin fondos suficientes en ninguna cuenta.")

    def listar_pagos(self):
        """Lista todos los pagos realizados en orden cronológico usando el iterador."""
        print("\n=== Historial de pagos (orden cronológico) ===")
        iterador = IteradorPagos(self._historial)
        for pago in iterador:
            print(f"  {pago}")
        print(f"Total de pagos realizados: {len(self._historial)}")

    def mostrar_saldos(self):
        """Muestra el saldo actual de cada cuenta."""
        print("\n=== Saldos actuales ===")
        print(f"  {self._cuenta1.token}: ${self._cuenta1.saldo:.2f}")
        print(f"  {self._cuenta2.token}: ${self._cuenta2.saldo:.2f}")


if __name__ == "__main__":

    print(f"Sistema de Pagos Automatizado - Versión {VERSION}")
    print("copyright UADER-FCyT-IS2©2024 todos los derechos reservados\n")

    gestor = GestorPagos()

    # Mostrar saldos iniciales
    gestor.mostrar_saldos()
    print()

    # Realizar pedidos de pago de $500 cada uno
    MONTO_PAGO = 500.0
    TOTAL_PEDIDOS = 6

    print("=== Procesando pedidos ===")
    for numero in range(1, TOTAL_PEDIDOS + 1):
        gestor.solicitar_pago(numero, MONTO_PAGO)

    # Mostrar saldos finales
    gestor.mostrar_saldos()

    # Listar todos los pagos con el iterador
    gestor.listar_pagos()
