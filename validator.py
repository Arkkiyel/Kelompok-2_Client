

class inputValidation:
    @staticmethod
    def ivString(value):
        if not isinstance(value, str):
            raise ValueError("Input harus berupa string.")
        return value
    @staticmethod
    def ivMatrix(value):
        if not isinstance(value, list):
            raise ValueError("Matriks harus berupa list.")

        if len(value) != 3:
            raise ValueError("Matriks harus memiliki 3 baris.")

        for row in value:
            if not isinstance(row, list):
                raise ValueError("Setiap baris matriks harus berupa list.")
            
            if len(row) != 3:
                raise ValueError("Setiap baris harus memiliki 3 elemen.")
            for element in row:
                if not isinstance(element,int):
                    raise ValueError("Tiap elemen matriks harus berupa angka.")
        return value
                