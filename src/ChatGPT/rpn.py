"""
rpn.py — Calculadora RPN (Reverse Polish Notation)
====================================================
Trabajo Práctico 2 · Ingeniería de Software II · Dr. Pedro E. Colla
Universidad Autónoma de Entre Ríos — FCyT

Características implementadas:
  1.  Pila interna para evaluación de expresiones.
  2.  Soporte de enteros y reales (incluyendo negativos).
  3.  Operaciones básicas: + - * /
  4.  Manejo de errores con excepción RPNError:
        - token inválido
        - pila insuficiente
        - división por cero
        - resultado distinto de 1 elemento en la pila
  5.  Comandos de pila: dup, swap, drop, clear
  6.  Constantes: p (π), e (número de Euler), j (φ — número áureo)
  7.  Funciones: sqrt, log, ln, ex, 10x, yx, 1/x
  8.  CHS (+/-): cambia el signo del tope de la pila
  9.  Trigonometría en grados: sin, cos, tg, asin, acos, atg
  10. 10 memorias (00–09) con comandos STO / RCL
  11. Soporte completo de floats y negativos en todas las ops
  12. Excepciones RPNError con mensajes descriptivos
  13. Validación: exactamente 1 elemento al final
  14. main() acepta expresión por argumento o stdin
  15. Solo stdlib — sin eval / exec
  16. Código corto y legible

Mejora v2 (ítem 6 del TP):
  - Las cadenas if/elif de _apply_binary, _apply_unary, _apply_trig y
    _apply_stack_cmd fueron reemplazadas por diccionarios de despacho
    (dispatch dicts). Esto reduce la complejidad ciclomática y hace el
    código más extensible: agregar una nueva operación implica solo añadir
    una entrada al diccionario, sin modificar la lógica de despacho.
"""

import math
import sys

# ---------------------------------------------------------------------------
# Excepción personalizada
# ---------------------------------------------------------------------------


class RPNError(Exception):
    """Excepción específica de la calculadora RPN."""


# ---------------------------------------------------------------------------
# Constantes predefinidas accesibles por nombre de token
# ---------------------------------------------------------------------------

CONSTANTS = {
    "p": math.pi,  # π — pi
    "e": math.e,  # e — número de Euler
    "j": (1 + math.sqrt(5)) / 2,  # φ — número áureo (phi)
}


# ---------------------------------------------------------------------------
# Funciones auxiliares con validación para operaciones que pueden fallar
# ---------------------------------------------------------------------------


def _safe_div(a: float, b: float) -> float:
    """División con control explícito de división por cero."""
    if b == 0:
        raise RPNError("División por cero")
    return a / b


def _safe_sqrt(a: float) -> float:
    """Raíz cuadrada; lanza RPNError si el argumento es negativo."""
    if a < 0:
        raise RPNError("sqrt de número negativo")
    return math.sqrt(a)


def _safe_log(a: float) -> float:
    """Logaritmo base 10; lanza RPNError si el argumento no es positivo."""
    if a <= 0:
        raise RPNError("log de número no positivo")
    return math.log10(a)


def _safe_ln(a: float) -> float:
    """Logaritmo natural; lanza RPNError si el argumento no es positivo."""
    if a <= 0:
        raise RPNError("ln de número no positivo")
    return math.log(a)


def _safe_inv(a: float) -> float:
    """Inverso (1/x); lanza RPNError si el argumento es cero."""
    if a == 0:
        raise RPNError("Inverso de cero (1/0)")
    return 1.0 / a


def _safe_asin(a: float) -> float:
    """Arcoseno en grados; valida que el argumento esté en [-1, 1]."""
    if not -1 <= a <= 1:
        raise RPNError("asin: argumento fuera de [-1, 1]")
    return math.degrees(math.asin(a))


def _safe_acos(a: float) -> float:
    """Arcocoseno en grados; valida que el argumento esté en [-1, 1]."""
    if not -1 <= a <= 1:
        raise RPNError("acos: argumento fuera de [-1, 1]")
    return math.degrees(math.acos(a))


# ---------------------------------------------------------------------------
# Tablas de despacho (dispatch dicts)
# Cada tabla mapea un token a la función que lo implementa.
# Esto reemplaza las cadenas if/elif, reduciendo la complejidad ciclomática.
# ---------------------------------------------------------------------------

# Operaciones binarias: reciben (a, b) y retornan el resultado
BINARY_OPS: dict = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "*": lambda a, b: a * b,
    "/": _safe_div,
    "yx": lambda a, b: a**b,  # a elevado a b
}

# Operaciones unarias: reciben (a,) y retornan el resultado
UNARY_OPS: dict = {
    "sqrt": _safe_sqrt,
    "log": _safe_log,  # logaritmo base 10
    "ln": _safe_ln,  # logaritmo natural
    "ex": math.exp,  # e elevado a x
    "10x": lambda a: 10**a,  # 10 elevado a x
    "1/x": _safe_inv,  # inverso multiplicativo
    "chs": lambda a: -a,  # cambio de signo (Change Sign)
}

# Funciones trigonométricas (entrada/salida en grados)
TRIG_OPS: dict = {
    "sin": lambda a: math.sin(math.radians(a)),
    "cos": lambda a: math.cos(math.radians(a)),
    "tg": lambda a: math.tan(math.radians(a)),
    "asin": _safe_asin,
    "acos": _safe_acos,
    "atg": lambda a: math.degrees(math.atan(a)),
}


# ---------------------------------------------------------------------------
# Clase principal: calculadora RPN
# ---------------------------------------------------------------------------


class RPNCalculator:
    """
    Evalúa expresiones en notación polaca inversa (RPN).

    La evaluación es token a token:
      - Si el token es un número lo apila.
      - Si es una constante conocida apila su valor.
      - Si es un operador / función lo ejecuta sobre la pila.
      - Si es un comando de pila (dup, swap, …) lo ejecuta.
      - Si es STO/RCL opera sobre las memorias.

    Las operaciones se despachan mediante diccionarios (BINARY_OPS,
    UNARY_OPS, TRIG_OPS) en lugar de cadenas if/elif, lo que reduce
    la complejidad ciclomática y facilita la extensión del programa.
    """

    def __init__(self) -> None:
        # Pila principal de trabajo
        self._stack: list[float] = []
        # Banco de 10 memorias numeradas "00" a "09"
        self._memory: dict[str, float] = {f"{i:02d}": 0.0 for i in range(10)}
        # Tabla de comandos de pila: cada comando es un método sin argumentos
        # Se define aquí para poder referenciar self
        self._stack_cmds: dict = {
            "dup": self._cmd_dup,
            "swap": self._cmd_swap,
            "drop": self._cmd_drop,
            "clear": self._cmd_clear,
        }

    # ------------------------------------------------------------------
    # Acceso controlado a la pila
    # ------------------------------------------------------------------

    def _push(self, value: float) -> None:
        """Apila un valor."""
        self._stack.append(value)

    def _pop(self, context: str = "operación") -> float:
        """
        Desapila y retorna el tope.
        Lanza RPNError si la pila está vacía.
        """
        if not self._stack:
            raise RPNError(f"Pila insuficiente para {context}")
        return self._stack.pop()

    def _peek(self) -> float:
        """Retorna el tope sin desapilar."""
        if not self._stack:
            raise RPNError("Pila vacía — no hay elemento en el tope")
        return self._stack[-1]

    # ------------------------------------------------------------------
    # Comandos de pila individuales (referenciados en _stack_cmds)
    # ------------------------------------------------------------------

    def _cmd_dup(self) -> None:
        """Duplica el tope de la pila."""
        self._push(self._peek())

    def _cmd_swap(self) -> None:
        """Intercambia los dos elementos superiores de la pila."""
        b = self._pop("swap")
        a = self._pop("swap")
        self._push(b)
        self._push(a)

    def _cmd_drop(self) -> None:
        """Descarta el tope de la pila."""
        self._pop("drop")

    def _cmd_clear(self) -> None:
        """Vacía toda la pila."""
        self._stack.clear()

    # ------------------------------------------------------------------
    # Despacho de operaciones usando los diccionarios globales
    # ------------------------------------------------------------------

    def _apply_binary(self, op: str) -> None:
        """Extrae dos operandos y aplica la operación binaria del dict."""
        b = self._pop(f"operador '{op}' (operando derecho)")
        a = self._pop(f"operador '{op}' (operando izquierdo)")
        # La función en el dict se encarga de la validación (ej: div/0)
        self._push(BINARY_OPS[op](a, b))

    def _apply_unary(self, op: str) -> None:
        """Extrae un operando y aplica la función unaria del dict."""
        a = self._pop(f"función '{op}'")
        # La función en el dict se encarga de la validación (ej: sqrt<0)
        self._push(UNARY_OPS[op](a))

    def _apply_trig(self, op: str) -> None:
        """Extrae un operando y aplica la función trigonométrica del dict."""
        a = self._pop(f"función trig '{op}'")
        self._push(TRIG_OPS[op](a))

    # ------------------------------------------------------------------
    # Memorias: STO <nn> / RCL <nn>
    # ------------------------------------------------------------------

    def _apply_sto(self, tokens: list[str], idx: int) -> int:
        """
        STO <nn>: guarda el tope de la pila en la memoria nn.
        Retorna el nuevo índice para continuar el parsing.
        """
        if idx >= len(tokens):
            raise RPNError("STO requiere un número de memoria (00–09)")
        slot = tokens[idx]
        if slot not in self._memory:
            raise RPNError(f"Memoria inválida '{slot}'; use 00–09")
        self._memory[slot] = self._peek()
        return idx + 1  # consumió el siguiente token

    def _apply_rcl(self, tokens: list[str], idx: int) -> int:
        """
        RCL <nn>: apila el valor de la memoria nn.
        Retorna el nuevo índice para continuar el parsing.
        """
        if idx >= len(tokens):
            raise RPNError("RCL requiere un número de memoria (00–09)")
        slot = tokens[idx]
        if slot not in self._memory:
            raise RPNError(f"Memoria inválida '{slot}'; use 00–09")
        self._push(self._memory[slot])
        return idx + 1  # consumió el siguiente token

    # ------------------------------------------------------------------
    # Evaluador principal
    # ------------------------------------------------------------------

    def evaluate(self, expression: str) -> float:
        """
        Evalúa la expresión RPN dada como cadena de texto.

        Args:
            expression: cadena con tokens separados por espacios.

        Returns:
            El único valor que queda en la pila tras la evaluación.

        Raises:
            RPNError: ante cualquier condición de error.
        """
        # Reiniciar la pila antes de cada evaluación
        self._stack.clear()

        tokens = expression.strip().split()
        if not tokens:
            raise RPNError("Expresión vacía")

        idx = 0
        while idx < len(tokens):
            token = tokens[idx].lower()

            if token in CONSTANTS:
                # Es una constante matemática → apilar su valor
                self._push(CONSTANTS[token])

            elif token in BINARY_OPS:
                # Operación binaria: despacho por diccionario
                self._apply_binary(token)

            elif token in UNARY_OPS:
                # Función unaria: despacho por diccionario
                self._apply_unary(token)

            elif token in TRIG_OPS:
                # Función trigonométrica: despacho por diccionario
                self._apply_trig(token)

            elif token in self._stack_cmds:
                # Comando de pila: despacho por diccionario
                self._stack_cmds[token]()

            elif token == "sto":
                idx = self._apply_sto(tokens, idx + 1)
                continue  # idx ya fue avanzado dentro del método

            elif token == "rcl":
                idx = self._apply_rcl(tokens, idx + 1)
                continue

            else:
                # Intentar interpretar como número (entero o float)
                try:
                    self._push(float(token))
                except ValueError:
                    raise RPNError(f"Token inválido: '{token}'") from None

            idx += 1

        # Validar que quede exactamente 1 valor en la pila
        if len(self._stack) != 1:
            raise RPNError(
                f"La pila debe tener exactamente 1 elemento al final, "
                f"pero tiene {len(self._stack)}: {self._stack}"
            )

        return self._stack[0]


# ---------------------------------------------------------------------------
# Punto de entrada
# ---------------------------------------------------------------------------


def main() -> None:
    """
    Acepta la expresión RPN por argumento de línea de comandos o por stdin.

    Uso:
        python rpn.py "3 4 +"
        echo "3 4 +" | python rpn.py
    """
    calc = RPNCalculator()

    # Si se pasó la expresión como argumento(s) en la línea de comandos
    if len(sys.argv) > 1:
        expression = " ".join(sys.argv[1:])
    else:
        # Leer desde stdin (pipe o input interactivo)
        expression = input("RPN> ").strip()

    try:
        result = calc.evaluate(expression)
        # Mostrar entero si el resultado no tiene parte decimal
        if result == int(result):
            print(int(result))
        else:
            print(result)
    except RPNError as err:
        print(f"Error: {err}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
