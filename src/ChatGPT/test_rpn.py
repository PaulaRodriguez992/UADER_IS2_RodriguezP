"""
test_rpn.py — Suite de tests unitarios para rpn.py
====================================================
Trabajo Práctico 2 · Ingeniería de Software II · Dr. Pedro E. Colla

Cobertura objetivo: ≥ 90%
Ejecutar con:
    coverage run -m unittest -v
    coverage report -m
    coverage report --fail-under=90
"""

import math
import sys
import unittest
from io import StringIO
from unittest.mock import patch

from rpn import RPNCalculator, RPNError, main


# ---------------------------------------------------------------------------
# Tests: operaciones básicas
# ---------------------------------------------------------------------------

class TestOperacionesBasicas(unittest.TestCase):
    """Prueba las cuatro operaciones aritméticas fundamentales."""

    def setUp(self):
        """Crea una calculadora fresca antes de cada test."""
        self.calc = RPNCalculator()

    def test_suma_enteros(self):
        self.assertEqual(self.calc.evaluate("3 4 +"), 7)

    def test_resta(self):
        self.assertEqual(self.calc.evaluate("10 3 -"), 7)

    def test_multiplicacion(self):
        self.assertEqual(self.calc.evaluate("3 4 *"), 12)

    def test_division(self):
        self.assertAlmostEqual(self.calc.evaluate("10 4 /"), 2.5)

    def test_expresion_compuesta_1(self):
        # 5 1 2 + 4 * + 3 - → 14
        self.assertEqual(self.calc.evaluate("5 1 2 + 4 * + 3 -"), 14)

    def test_expresion_compuesta_2(self):
        # 2 3 4 * + → 14
        self.assertEqual(self.calc.evaluate("2 3 4 * +"), 14)

    def test_numeros_negativos(self):
        self.assertEqual(self.calc.evaluate("-3 -4 +"), -7)

    def test_numeros_reales(self):
        self.assertAlmostEqual(self.calc.evaluate("2.5 1.5 +"), 4.0)

    def test_potencia_yx(self):
        self.assertAlmostEqual(self.calc.evaluate("2 10 yx"), 1024)


# ---------------------------------------------------------------------------
# Tests: manejo de errores (consigna 4 y 12)
# ---------------------------------------------------------------------------

class TestErrores(unittest.TestCase):
    """Prueba que RPNError se lanza correctamente ante entradas inválidas."""

    def setUp(self):
        self.calc = RPNCalculator()

    def test_division_por_cero(self):
        with self.assertRaises(RPNError) as ctx:
            self.calc.evaluate("3 0 /")
        self.assertIn("cero", str(ctx.exception).lower())

    def test_token_invalido(self):
        with self.assertRaises(RPNError) as ctx:
            self.calc.evaluate("3 4 @")
        self.assertIn("inválido", str(ctx.exception))

    def test_pila_insuficiente_suma(self):
        with self.assertRaises(RPNError):
            self.calc.evaluate("3 +")

    def test_pila_insuficiente_resta(self):
        with self.assertRaises(RPNError):
            self.calc.evaluate("5 -")

    def test_pila_insuficiente_mul(self):
        with self.assertRaises(RPNError):
            self.calc.evaluate("5 *")

    def test_pila_insuficiente_div(self):
        with self.assertRaises(RPNError):
            self.calc.evaluate("5 /")

    def test_multiples_valores_al_final(self):
        # Quedan 2 valores en la pila → error
        with self.assertRaises(RPNError) as ctx:
            self.calc.evaluate("3 4")
        self.assertIn("exactamente", str(ctx.exception))

    def test_expresion_vacia(self):
        with self.assertRaises(RPNError):
            self.calc.evaluate("")

    def test_expresion_solo_espacios(self):
        with self.assertRaises(RPNError):
            self.calc.evaluate("   ")

    def test_pila_vacia_peek(self):
        # drop sobre pila vacía debe fallar
        with self.assertRaises(RPNError):
            self.calc.evaluate("drop")

    def test_sqrt_negativo(self):
        with self.assertRaises(RPNError):
            self.calc.evaluate("-4 sqrt")

    def test_log_no_positivo(self):
        with self.assertRaises(RPNError):
            self.calc.evaluate("0 log")

    def test_ln_no_positivo(self):
        with self.assertRaises(RPNError):
            self.calc.evaluate("-1 ln")

    def test_inverso_de_cero(self):
        with self.assertRaises(RPNError):
            self.calc.evaluate("0 1/x")

    def test_asin_fuera_de_rango(self):
        with self.assertRaises(RPNError):
            self.calc.evaluate("2 asin")

    def test_acos_fuera_de_rango(self):
        with self.assertRaises(RPNError):
            self.calc.evaluate("-2 acos")


# ---------------------------------------------------------------------------
# Tests: comandos de pila (consigna 5)
# ---------------------------------------------------------------------------

class TestComandosPila(unittest.TestCase):

    def setUp(self):
        self.calc = RPNCalculator()

    def test_dup(self):
        # dup duplica el tope; luego + da el doble
        self.assertEqual(self.calc.evaluate("7 dup +"), 14)

    def test_swap(self):
        # swap intercambia: 3 5 swap → tope=3; luego 3-5 = -2
        self.assertEqual(self.calc.evaluate("3 5 swap -"), 2)

    def test_drop(self):
        # drop descarta el tope; queda 3
        self.assertEqual(self.calc.evaluate("3 99 drop"), 3)

    def test_clear(self):
        # clear vacía la pila; luego apilamos un solo valor
        self.assertEqual(self.calc.evaluate("1 2 3 clear 42"), 42)

    def test_swap_pila_insuficiente(self):
        with self.assertRaises(RPNError):
            self.calc.evaluate("5 swap")


# ---------------------------------------------------------------------------
# Tests: constantes (consigna 6)
# ---------------------------------------------------------------------------

class TestConstantes(unittest.TestCase):

    def setUp(self):
        self.calc = RPNCalculator()

    def test_pi(self):
        self.assertAlmostEqual(self.calc.evaluate("p"), math.pi)

    def test_euler(self):
        self.assertAlmostEqual(self.calc.evaluate("e"), math.e)

    def test_phi(self):
        phi = (1 + math.sqrt(5)) / 2
        self.assertAlmostEqual(self.calc.evaluate("j"), phi)

    def test_constante_en_expresion(self):
        # p * p → π²
        self.assertAlmostEqual(self.calc.evaluate("p p *"), math.pi**2)


# ---------------------------------------------------------------------------
# Tests: funciones matemáticas (consigna 7)
# ---------------------------------------------------------------------------

class TestFunciones(unittest.TestCase):

    def setUp(self):
        self.calc = RPNCalculator()

    def test_sqrt(self):
        self.assertAlmostEqual(self.calc.evaluate("9 sqrt"), 3.0)

    def test_log(self):
        self.assertAlmostEqual(self.calc.evaluate("100 log"), 2.0)

    def test_ln(self):
        self.assertAlmostEqual(self.calc.evaluate("1 ln"), 0.0)

    def test_ex(self):
        self.assertAlmostEqual(self.calc.evaluate("1 ex"), math.e)

    def test_10x(self):
        self.assertAlmostEqual(self.calc.evaluate("3 10x"), 1000.0)

    def test_inverso(self):
        self.assertAlmostEqual(self.calc.evaluate("4 1/x"), 0.25)

    def test_yx(self):
        self.assertAlmostEqual(self.calc.evaluate("3 3 yx"), 27.0)


# ---------------------------------------------------------------------------
# Tests: CHS — cambio de signo (consigna 8)
# ---------------------------------------------------------------------------

class TestCHS(unittest.TestCase):

    def setUp(self):
        self.calc = RPNCalculator()

    def test_chs_positivo_a_negativo(self):
        self.assertEqual(self.calc.evaluate("5 chs"), -5)

    def test_chs_negativo_a_positivo(self):
        self.assertEqual(self.calc.evaluate("-7 chs"), 7)

    def test_chs_doble_es_identidad(self):
        self.assertEqual(self.calc.evaluate("3 chs chs"), 3)


# ---------------------------------------------------------------------------
# Tests: trigonometría en grados (consigna 9)
# ---------------------------------------------------------------------------

class TestTrigonometria(unittest.TestCase):

    def setUp(self):
        self.calc = RPNCalculator()

    def test_sin_90(self):
        self.assertAlmostEqual(self.calc.evaluate("90 sin"), 1.0)

    def test_sin_0(self):
        self.assertAlmostEqual(self.calc.evaluate("0 sin"), 0.0)

    def test_cos_0(self):
        self.assertAlmostEqual(self.calc.evaluate("0 cos"), 1.0)

    def test_cos_90(self):
        self.assertAlmostEqual(self.calc.evaluate("90 cos"), 0.0, places=10)

    def test_tg_45(self):
        self.assertAlmostEqual(self.calc.evaluate("45 tg"), 1.0)

    def test_asin_1(self):
        self.assertAlmostEqual(self.calc.evaluate("1 asin"), 90.0)

    def test_acos_1(self):
        self.assertAlmostEqual(self.calc.evaluate("1 acos"), 0.0)

    def test_atg_1(self):
        self.assertAlmostEqual(self.calc.evaluate("1 atg"), 45.0)


# ---------------------------------------------------------------------------
# Tests: memorias STO / RCL (consigna 10)
# ---------------------------------------------------------------------------

class TestMemorias(unittest.TestCase):

    def setUp(self):
        self.calc = RPNCalculator()

    def test_sto_rcl_basico(self):
        # Guardar 42 en memoria 00, vaciar pila, recuperar
        self.assertEqual(self.calc.evaluate("42 sto 00 clear rcl 00"), 42)

    def test_memoria_inicial_es_cero(self):
        self.assertEqual(self.calc.evaluate("rcl 05"), 0.0)

    def test_sto_sin_slot(self):
        with self.assertRaises(RPNError):
            self.calc.evaluate("5 sto")

    def test_rcl_sin_slot(self):
        with self.assertRaises(RPNError):
            self.calc.evaluate("rcl")

    def test_sto_slot_invalido(self):
        with self.assertRaises(RPNError):
            self.calc.evaluate("5 sto 99")

    def test_rcl_slot_invalido(self):
        with self.assertRaises(RPNError):
            self.calc.evaluate("rcl 99")

    def test_multiples_memorias(self):
        # Usar dos memorias distintas
        result = self.calc.evaluate("10 sto 01 20 sto 02 clear rcl 01 rcl 02 +")
        self.assertEqual(result, 30)


# ---------------------------------------------------------------------------
# Tests: función main() — argumento y stdin (consigna 14)
# ---------------------------------------------------------------------------

class TestMain(unittest.TestCase):

    def test_main_con_argumento(self):
        """main() debe imprimir el resultado cuando se pasa por argv."""
        with patch("sys.argv", ["rpn.py", "3", "4", "+"]):
            with patch("sys.stdout", new_callable=StringIO) as mock_out:
                main()
        self.assertEqual(mock_out.getvalue().strip(), "7")

    def test_main_resultado_float(self):
        """Resultado real debe imprimirse como float."""
        with patch("sys.argv", ["rpn.py", "10", "4", "/"]):
            with patch("sys.stdout", new_callable=StringIO) as mock_out:
                main()
        self.assertIn("2.5", mock_out.getvalue())

    def test_main_stdin(self):
        """main() debe leer de stdin cuando no hay argumentos."""
        with patch("sys.argv", ["rpn.py"]):
            with patch("builtins.input", return_value="5 3 +"):
                with patch("sys.stdout", new_callable=StringIO) as mock_out:
                    main()
        self.assertEqual(mock_out.getvalue().strip(), "8")

    def test_main_error_imprime_stderr_y_sale(self):
        """main() debe escribir en stderr y salir con código 1 ante error."""
        with patch("sys.argv", ["rpn.py", "3", "0", "/"]):
            with patch("sys.stderr", new_callable=StringIO):
                with self.assertRaises(SystemExit) as ctx:
                    main()
        self.assertEqual(ctx.exception.code, 1)


# ---------------------------------------------------------------------------
# Tests: mayúsculas/minúsculas (robustez de parsing)
# ---------------------------------------------------------------------------

class TestCaseSensitivity(unittest.TestCase):

    def setUp(self):
        self.calc = RPNCalculator()

    def test_operadores_en_mayuscula(self):
        # Los tokens se convierten a lowercase internamente
        self.assertAlmostEqual(self.calc.evaluate("9 SQRT"), 3.0)

    def test_constante_mayuscula(self):
        self.assertAlmostEqual(self.calc.evaluate("P"), math.pi)


# ---------------------------------------------------------------------------
# Punto de entrada
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main(verbosity=2)
