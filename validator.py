import numpy as np


class inputValidation:
    @staticmethod
    def ivString(value):
        if not isinstance(value, str):
            raise ValueError("Input harus berupa string.")
        if not value.strip():
            raise ValueError("Input string tidak boleh kosong.")
        return value

    @staticmethod
    def ivMatrix(value):
        if not isinstance(value, list) or len(value) != 3:
            raise ValueError("Matriks harus berupa list 3 baris.")

        for row in value:
            if not isinstance(row, list) or len(row) != 3:
                raise ValueError("Setiap baris matriks harus berupa list 3 elemen.")
            for element in row:
                if not isinstance(element, (int, float)):
                    raise ValueError("Tiap elemen matriks harus berupa angka.")
        return value


def verify_result(service, request_data, server_result):
    try:
        if service == "CHAR_COUNT":
            return len(str(request_data)) == server_result

        elif service == "WORD_COUNT":
            return len(str(request_data).split()) == server_result

        elif service == "REVERSE_STRING":  # Disesuaikan dengan server
            return str(request_data)[::-1] == server_result

        elif service == "REMOVE_VOWELS":
            vowels = "aeiouAEIOU"
            expected = "".join([c for c in str(request_data) if c not in vowels])
            return expected == server_result

        elif service == "MATRIX_3X3":
            if not isinstance(server_result, dict):
                return False

            mat = np.array(request_data, dtype=float)
            expected_det = float(np.linalg.det(mat))

            server_det = server_result.get("determinant")
            server_inv = server_result.get("inverse")

            if server_det is None or not np.isclose(expected_det, server_det, atol=1e-3):
                return False

            if np.isclose(expected_det, 0):
                return server_inv is None
            else:
                if server_inv is None:
                    return False
                expected_inv = np.linalg.inv(mat)
                server_inv_mat = np.array(server_inv, dtype=float)
                return np.allclose(expected_inv, server_inv_mat, atol=1e-3)

        return False
    except Exception:
        return False