import unittest

from new_primes_v4 import es_primo, obtener_primos_en_rango  # Suponiendo nombre del archivo `programa.py`

class TestFuncionesPrimos(unittest.TestCase):
    def test_es_primo(self):
        self.assertFalse(es_primo(0))
        self.assertFalse(es_primo(1))
        self.assertTrue(es_primo(2))
        self.assertTrue(es_primo(3))
        self.assertFalse(es_primo(4))
        self.assertTrue(es_primo(29))
    
    def test_obtener_primos_en_rango(self):
        self.assertEqual(obtener_primos_en_rango(1, 10), [2, 3, 5, 7])
        self.assertEqual(obtener_primos_en_rango(10, 10), [])
        self.assertEqual(obtener_primos_en_rango(11, 11), [11])
        self.assertEqual(obtener_primos_en_rango(20, 23), [23])
        self.assertEqual(obtener_primos_en_rango(30, 29), [])  # Rango inválido

if __name__ == "__main__":
    unittest.main()

