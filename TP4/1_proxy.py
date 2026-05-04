#*------------------------------------------------------------------------
#* Ingeniería de Software II
#* Patrones Estructurales
#* Proxy - TP4 Punto 1
#* UADER - Ingeniería de Software II
#* Rodriguez Paula
#*------------------------------------------------------------------------

# El patrón Proxy coloca un intermediario entre el cliente y el objeto real.
# El cliente nunca habla directamente con el objeto real: siempre pasa por el proxy,
# que puede restringir, redirigir o agregar lógica antes de delegar la llamada.

import os
import platform

class ping:
    """
    Objeto real.
    Es quien realmente sabe ejecutar un ping.
    El cliente no lo usa directamente; el proxy decide cuándo y cómo llamarlo.
    """

    def _do_ping(self, host: str, count: int) -> None:
        """
        Método interno compartido por execute() y executefree().
        Detecta el sistema operativo para usar el parámetro correcto:
          -n  en Windows
          -c  en Linux / macOS
        """
        param = "-n" if platform.system() == "Windows" else "-c"
        print(f"\nEjecutando ping a {host} ({count} intentos)...")
        os.system(f"ping {param} {count} {host}")

    def execute(self, string: str) -> None:
        """
        Ping con restricción:
        Solo ejecuta el ping si la dirección IP comienza con '192.'
        Si no cumple la condición, informa y sale sin hacer nada.
        """
        if not string.startswith("192."):
            print(f"[ping] Acceso denegado: '{string}' no comienza con '192.'")
            return
        # Si pasó la validación, delega al método interno
        self._do_ping(string, 10)

    def executefree(self, string: str) -> None:
        """
        Ping sin restricción:
        Acepta cualquier dirección sin validar. Se usa cuando el proxy
        necesita redirigir a un host externo como www.google.com.
        """
        self._do_ping(string, 10)


class pingproxy:
    """
    Proxy.
    Intercepta todas las llamadas a execute() y decide el enrutamiento:
      - Si la IP es '192.168.0.254' → caso especial: redirige a www.google.com
        usando executefree() del objeto real (saltea la restricción de IP).
      - Cualquier otra IP → delega normalmente a execute() del objeto real,
        que aplicará su propia validación de prefijo '192.'.

    El cliente solo conoce al proxy; no sabe que existe la clase ping por detrás.
    """

    def __init__(self):
        # El proxy crea internamente el objeto real y lo guarda
        self._ping = ping()

    def execute(self, string: str) -> None:
        print(f"\n[pingproxy] Solicitud recibida para: {string}")

        if string == "192.168.0.254":
            # Caso especial definido en el enunciado:
            # Esta IP particular se redirige a Google usando executefree
            print("[pingproxy] Dirección especial detectada. Redirigiendo a www.google.com")
            self._ping.executefree("www.google.com")
        else:
            # Caso general: delega al objeto real con su restricción habitual
            self._ping.execute(string)


# =============================================================================
# Punto de entrada
# =============================================================================

if __name__ == "__main__":
    os.system("cls" if platform.system() == "Windows" else "clear")

    # El cliente solo instancia el proxy, nunca a ping directamente
    proxy = pingproxy()

    print("=== Caso 1: IP válida normal ===")
    # Empieza con '192.' → execute() de ping la acepta
    proxy.execute("192.168.1.1")

    print("\n=== Caso 2: IP especial (redirige a Google) ===")
    # El proxy detecta esta IP y usa executefree hacia www.google.com
    proxy.execute("192.168.0.254")

    print("\n=== Caso 3: IP no permitida (no empieza con 192.) ===")
    # El proxy delega a execute() de ping, que rechaza la dirección
    proxy.execute("10.0.0.1")