import unittest
from src.validator import verify_result

class TestValidator(unittest.TestCase):

    def test_char_count(self):
        service = "CHAR_COUNT"
        data = "Halo Dunia"
        
        # Skenario Benar (10 karakter)
        self.assertTrue(verify_result(service, data, 10))
        # Skenario Salah
        self.assertFalse(verify_result(service, data, 12))

    def test_word_count(self):
        service = "WORD_COUNT"
        data = "Halo Dunia Pemrograman"
        
        # Skenario Benar (3 kata)
        self.assertTrue(verify_result(service, data, 3))
        # Skenario Salah
        self.assertFalse(verify_result(service, data, 4))

    def test_reverse_str(self):
        service = "REVERSE_STR"
        data = "Python"
        
        # Skenario Benar
        self.assertTrue(verify_result(service, data, "nohtyP"))
        # Skenario Salah
        self.assertFalse(verify_result(service, data, "python"))

    def test_remove_vowels(self):
        service = "REMOVE_VOWELS"
        data = "Jaringan Komputer"
        
        # Skenario Benar (tanpa a, i, u, e, o)
        self.assertTrue(verify_result(service, data, "Jrngn Kmptr"))
        # Skenario Salah
        self.assertFalse(verify_result(service, data, "Jaringan Kmptr"))

    def test_matrix_3x3(self):
        service = "MATRIX_3X3"
        # Matriks dengan determinan = 1
        data = [
            [1, 2, 3],
            [0, 1, 4],
            [5, 6, 0]
        ]
        
        # Hasil invers yang diekspektasikan
        correct_inverse = [
            [-24.0, 18.0, 5.0],
            [20.0, -15.0, -4.0],
            [-5.0, 4.0, 1.0]
        ]
        
        correct_response = {
            "determinant": 1.0,
            "inverse": correct_inverse
        }
        
        incorrect_response = {
            "determinant": 0.0,
            "inverse": None
        }

        # Skenario Benar
        self.assertTrue(verify_result(service, data, correct_response))
        # Skenario Salah
        self.assertFalse(verify_result(service, data, incorrect_response))

if __name__ == '__main__':
    unittest.main()