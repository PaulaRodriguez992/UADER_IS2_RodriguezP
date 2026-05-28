# Ejemplo práctico de aplicación de patrón chain of responsibility
#*------------------------------------------------------------------------
#* Ingeniería de Software II
#* Patrones de Creación
#* Chain of responsibility
#* UADER - Ingeniería de Software II
#* Dr. Pedro E. Colla
#*------------------------------------------------------------------------
"""
Este patrón aparece muchísimo en sistemas reales:

	🔍 Validaciones
		pipelines de validación (input, negocio, seguridad)
	🌐 Middleware (muy importante)
		frameworks web (auth → logging → routing → handler)
	💳 Procesamiento financiero
		antifraude → scoring → autorización
	🧪 Testing / calidad
		filtros de errores
		clasificación de defectos
	📩 Manejo de eventos
		listeners encadenados

Chain of Responsibility desacopla quién envía una solicitud de quién la procesa.
👉 “Paso el problema a lo largo de la cadena hasta que alguien lo resuelva.”

🔁 Comparación rápida con otros patrones que viste

Decorator: agrega comportamiento en cadena, pero todos ejecutan
Chain of Responsibility: solo uno maneja (o decide escalar)
Facade: simplifica acceso, no distribuye responsabilidad
Proxy: controla acceso, no delega múltiples manejadores
"""
from abc import ABC, abstractmethod


class Solicitud:
    """Representa una solicitud de gasto."""

    def __init__(self, empleado: str, monto: float) -> None:
        self.empleado = empleado
        self.monto = monto


class Aprobador(ABC):
    """
    Handler abstracto.

    Mantiene referencia al siguiente en la cadena.
    """

    def __init__(self) -> None:
        self._siguiente: "Aprobador" | None = None

    def establecer_siguiente(self, aprobador: "Aprobador") -> "Aprobador":
        self._siguiente = aprobador
        return aprobador  # permite encadenar

    @abstractmethod
    def manejar(self, solicitud: Solicitud) -> None:
        pass


class Supervisor(Aprobador):
    def manejar(self, solicitud: Solicitud) -> None:
        if solicitud.monto <= 10000:
            print(
                f"[Supervisor] Aprobada solicitud de "
                f"${solicitud.monto:.2f} para {solicitud.empleado}"
            )
        elif self._siguiente:
            print("[Supervisor] Escalando al gerente...")
            self._siguiente.manejar(solicitud)


class Gerente(Aprobador):
    def manejar(self, solicitud: Solicitud) -> None:
        if solicitud.monto <= 50000:
            print(
                f"[Gerente] Aprobada solicitud de "
                f"${solicitud.monto:.2f} para {solicitud.empleado}"
            )
        elif self._siguiente:
            print("[Gerente] Escalando al director...")
            self._siguiente.manejar(solicitud)


class Director(Aprobador):
    def manejar(self, solicitud: Solicitud) -> None:
        print(
            f"[Director] Aprobada solicitud de "
            f"${solicitud.monto:.2f} para {solicitud.empleado}"
        )


def main() -> None:
    # Construcción de la cadena
    supervisor = Supervisor()
    gerente = Gerente()
    director = Director()

    supervisor.establecer_siguiente(director)

    # Casos de prueba
    solicitudes = [
        Solicitud("Ana", 5000),
        Solicitud("Luis", 20000),
        Solicitud("María", 120000),
    ]

    for s in solicitudes:
        print("\nProcesando solicitud...")
        supervisor.manejar(s)


if __name__ == "__main__":
    main()
