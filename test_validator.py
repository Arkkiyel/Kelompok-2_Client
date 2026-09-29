import unittest
from validator import verify_result, inputValidation

class TestValidator(unittest.TestCase):

    def test_char_count(self):
        self.assertTrue(verify_result("CHAR_COUNT", "Hello World", 11))
        self.assertFalse(verify_result("CHAR_COUNT", "Hello World", 5))

    def test_word_count(self):
        self.assertTrue(verify_result("WORD_COUNT", "Jaringan Komputer TCP", 3))
        self.assertFalse(verify_result("WORD_COUNT", "Jaringan Komputer TCP", 5))

    def test_reverse_str(self):
        self.assertTrue(verify_result("REVERSE_STRING", "Python", "nohtyP"))
        self.assertFalse(verify_result("REVERSE_STRING", "Python", "Python"))

    def test_remove_vowels(self):
        self.assertTrue(verify_result("REMOVE_VOWELS", "Jaringan Komputer", "Jrngn Kmptr"))
        self.assertFalse(verify_result("REMOVE_VOWELS", "Jaringan Komputer", "Jaringan"))

    def test_matrix_3x3(self):
        mat = [[1, 2, 3], [0, 1, 4], [5, 6, 0]]
        correct_det = 1.0
        correct_inv = [[-24.0, 18.0, 5.0], [20.0, -15.0, -4.0], [-5.0, 4.0, 1.0]]
        correct_resp = {"determinant": correct_det, "inverse": correct_inv}

        self.assertTrue(verify_result("MATRIX_3X3", mat, correct_resp))

        wrong_resp = {"determinant": 99.0, "inverse": correct_inv}
        self.assertFalse(verify_result("MATRIX_3X3", mat, wrong_resp))

    def test_input_validation_string(self):
        self.assertEqual(inputValidation.ivString("Halo"), "Halo")
        with self.assertRaises(ValueError):
            inputValidation.ivString("")
        with self.assertRaises(ValueError):
            inputValidation.ivString(123)

    def test_input_validation_matrix(self):
        valid_mat = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        self.assertEqual(inputValidation.ivMatrix(valid_mat), valid_mat)

        with self.assertRaises(ValueError):
            inputValidation.ivMatrix([[1, 2], [3, 4]])
        with self.assertRaises(ValueError):
            inputValidation.ivMatrix([[1, "a", 3], [4, 5, 6], [7, 8, 9]])

if __name__ == "__main__":
    unittest.main()
