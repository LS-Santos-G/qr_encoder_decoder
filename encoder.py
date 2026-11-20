import numpy as np
from matplotlib import pyplot as plt
from reedsolo import RSCodec


# qr ver 1
qr_specs = {
    'L': {
        'ec_per_block': 7,
        'char_capacity':17,
        'max_num_bits': 8*19
    },
    'M': {
        'ec_per_block': 10,
        'char_capacity':14,
        'max_num_bits': 8*16
    },
    'Q': {
        'ec_per_block': 13,
        'char_capacity':11,
        'max_num_bits': 8*13
    },
    'H': {
        'ec_per_block': 17,
        'char_capacity': 7,
        'max_num_bits': 8*9
    }
}


class Encoder:


    message: str
    error_correction: str


    def __init__(self, message: str, error_correction: str):
        self.message = message
        # correcion seleccionada
        self.error_correction = qr_specs[error_correction]
        self.error_correction_level = error_correction
        self.encoded_message = ''


    # largo del texto como numero binario de 8 bits
    def encode_string_text(self):
        mode_indicator = '0100' # modo byte

        if(len(self.message) > self.error_correction['char_capacity']):
            print('El mensaje es muy largo para este nivel!')
            return -1

        char_count_indicator = f"{len(self.message):08b}"  # len del mensaje en binario, 8 bits
        messsage_binary = "".join(
        [f"{ord(char):08b}" for char in self.message])  # mensaje en binario, cada char de 8 bits

        # junta los strings anteriores
        encoded_message = mode_indicator + char_count_indicator + messsage_binary

        # cadenas faltantes
        max_num_bits = self.error_correction['max_num_bits']  # numero de bits maximo,

        # agrega los bits terminales necesarios
        if len(encoded_message) > max_num_bits:  # PON ALGO EN LA INTERFAZ
            print('No se puede!')
            return -1
        else:
            difference = max_num_bits - len(encoded_message)
            if difference > 4:
                encoded_message += '0'*4
            else:
                encoded_message += '0' * difference

        # hace que el largo del string sea multiplo de 8
        r = len(encoded_message) % 8
        if r != 0:
            encoded_message += '0'*(8-r)

        # llena la string hasta llegar al maximo permitido
        if len(encoded_message) != max_num_bits:
            needed = max_num_bits - len(encoded_message)
            pad_bytes = '1110110000010001'
            repeats = (needed + len(pad_bytes) - 1) // len(pad_bytes)

            padding = (pad_bytes * repeats)[:needed]

            encoded_message += padding

        self.encoded_message = encoded_message
        return 1


    def ger_ec_codewords(self) -> str:
        # Convierte cada grupo de 8 bits en un byte.
        data_bytes = bytes(
            int(self.encoded_message[i:i + 8], 2)
            for i in range(0, len(self.encoded_message), 8)
        )

        rs = RSCodec(self.error_correction["ec_per_block"])

        # Incluye los datos originales seguidos de su corrección.
        encoded_bytes = rs.encode(data_bytes)

        return "".join(f"{byte:08b}" for byte in encoded_bytes)


    def draw_finder_pattern(self, matrix, row_start, col_start):
        for i in range(7):
            for j in range(7):
                # Determine if the current module should be black (1) or white (0)
                # Outer border (i=0,6 or j=0,6) or inner block (2 <= i,j <= 4)
                is_outer = (i == 0 or i == 6 or j == 0 or j == 6)
                is_inner = (2 <= i <= 4 and 2 <= j <= 4)

                if is_outer or is_inner:
                    matrix[row_start + i, col_start + j] = 1
                else:
                    matrix[row_start + i, col_start + j] = 0


    def draw_timing_patterns(self, matrix):
        for i in range(8, 13):
            matrix[i][6] = 1 if i % 2 == 0 else 0
            matrix[6][i] = 1 if i % 2 == 0 else 0


    def place_data(self, matrix):
        pass


    def format_matrix(self):
        matrix = np.full((21, 21), -1, dtype=int)

        matrix[:8, :8] = 0
        matrix[:8, -8:] = 0
        matrix[-8:, :8] = 0

        # los cuadrados de las ezquinas
        self.draw_finder_pattern(matrix, 0, 0)
        self.draw_finder_pattern(matrix, 0, 14)
        self.draw_finder_pattern(matrix, 14, 0)

        self.draw_timing_patterns(matrix) #las rayas

        matrix[:8, 13] = 0
        matrix[7, 13:21] = 0

        #puntico (dark module)
        matrix[4+9][8] = 1

        '''
            Formato junto al cuadrado superior izquierdo. Uso -2 para indicar espacios reservados para 
            los bits del formato
        '''
        matrix[8, :6] = -2
        matrix[8, 7:9] = -2
        matrix[:6, 8] = -2
        matrix[7, 8] = -2

        # Segunda copia del formato.
        matrix[8, -8:] = -2
        matrix[-7:, 8] = -2

        return matrix
    # pone la información tras poner el formato


    def apply_mask(self, filled_matrix: np.ndarray, original_matrix: np.ndarray, mask_id: int) -> np.ndarray:
        if mask_id not in range(8):
            raise ValueError("La máscara debe estar entre 0 y 7.")

        masked_matrix = filled_matrix.copy()
        size = masked_matrix.shape[0]

        invert: bool = False

        for row in range(size):
            for col in range(size):
                if original_matrix[row, col] != -1:
                    continue

                match mask_id:
                    case 0:
                        invert = (row + col) % 2 == 0
                    case 1:
                        invert = row % 2 == 0
                    case 2:
                        invert = col % 3 == 0
                    case 3:
                        invert = (row + col) % 3 == 0
                    case 4:
                        invert = (row // 2 + col // 3) % 2 == 0
                    case 5:
                        invert = (row * col) % 2 + (row * col) % 3 == 0
                    case 6:
                        invert = ((row * col) % 2 + (row * col) % 3) % 2 == 0
                    case 7:
                        invert = ((row + col) % 2 + (row * col) % 3) % 2 == 0

                if invert:
                    masked_matrix[row, col] = 1 - masked_matrix[row, col]

        return masked_matrix


    def get_format_bits(self, mask_id: int) -> str:
        if mask_id not in range(8):
            raise ValueError("La máscara debe estar entre 0 y 7.")

        level_values = {"L": 1, "M": 0, "Q": 3, "H": 2}
        level = level_values[self.error_correction_level]

        # Dos bits de nivel y tres bits de máscara.
        data = (level << 3) | mask_id

        # División polinómica binaria para obtener la protección.
        remainder = data << 10
        generator = 0b10100110111

        for position in range(14, 9, -1):
            if (remainder >> position) & 1:
                remainder ^= generator << (position - 10)

        format_value = ((data << 10) | remainder) ^ 0b101010000010010

        return f"{format_value:015b}"


    def place_format_bits(self, matrix: np.ndarray, mask_id: int) -> np.ndarray:
        result = matrix.copy()
        size = result.shape[0]
        bits = self.get_format_bits(mask_id)[::-1]

        first_copy = (
                [(row, 8) for row in range(6)]
                + [(7, 8), (8, 8), (8, 7)]
                + [(8, col) for col in range(5, -1, -1)]
        )

        second_copy = (
                [(8, col) for col in range(size - 1, size - 9, -1)]
                + [(row, 8) for row in range(size - 7, size)]
        )

        for index, bit in enumerate(bits):
            row, col = first_copy[index]
            result[row, col] = int(bit)

            row, col = second_copy[index]
            result[row, col] = int(bit)

        return result


    def select_best_mask(self, filled_matrix: np.ndarray, original_matrix: np.ndarray) -> tuple[np.ndarray, int]:
        best_matrix = filled_matrix.copy()
        best_mask = 0
        best_penalty = float("inf")

        for mask_id in range(8):
            candidate = self.apply_mask(
                filled_matrix, original_matrix, mask_id
            )
            candidate = self.place_format_bits(candidate, mask_id)
            penalty = self.calculate_penalty(candidate)

            if penalty < best_penalty:
                best_penalty = penalty
                best_mask = mask_id
                best_matrix = candidate

        return best_matrix, best_mask


    def calculate_penalty(self, matrix: np.ndarray) -> int:
        penalty1: int = self.penalty_rule_1(matrix)
        penalty2: int = self.penalty_rule_2(matrix)
        penalty3: int = self.penalty_rule_3(matrix)
        penalty4: int = self.penalty_rule_4(matrix)

        return penalty1 + penalty2 + penalty3 + penalty4


    def penalty_rule_1(self, matrix: np.ndarray) -> int:
        penalty = 0

        # Revisa primero las filas y después las columnas.
        for lines in (matrix, matrix.T):
            for line in lines:
                consecutive = 1

                for index in range(1, len(line)):
                    if line[index] == line[index - 1]:
                        consecutive += 1

                        if consecutive == 5:
                            penalty += 3
                        elif consecutive > 5:
                            penalty += 1
                    else:
                        consecutive = 1

        return penalty


    def penalty_rule_2(self, matrix: np.ndarray) -> int:
        penalty = 0
        size = matrix.shape[0]

        for row in range(size - 1):
            for col in range(size - 1):
                color = matrix[row, col]

                if (
                        matrix[row, col + 1] == color
                        and matrix[row + 1, col] == color
                        and matrix[row + 1, col + 1] == color
                ):
                    penalty += 3

        return penalty


    def penalty_rule_3(self, matrix: np.ndarray) -> int:
        penalty = 0
        patterns = ("10111010000", "00001011101")

        for lines in (matrix, matrix.T):
            for line in lines:
                bits = "".join(str(int(value)) for value in line)

                for index in range(len(bits) - 10):
                    if bits[index:index + 11] in patterns:
                        penalty += 40

        return penalty


    def penalty_rule_4(self, matrix: np.ndarray) -> int:
        dark_modules = int(np.count_nonzero(matrix == 1))
        total_modules = matrix.size

        deviation = abs(dark_modules * 100 - total_modules * 50)
        steps = deviation // (total_modules * 5)

        return steps * 10


    def place_qr_data_bits(self, matrix: np.ndarray, encoded_bits: str) -> np.ndarray:
        # copy to avoid mutating the original array in-place unexpectedly
        matrix = matrix.copy()
        size = matrix.shape[0]
        bit_iter = iter(encoded_bits)

        # QR code bit placement starts from the bottom-right corner
        col = size - 1
        going_up = True

        while col > 0:
            # Column 6 is reserved for the vertical timing pattern; skip it and shift to column 5
            if col == 6:
                col -= 1

            # Determine row traversal direction based on the zigzag pattern
            row_range = range(size - 1, -1, -1) if going_up else range(0, size)

            for row in row_range:
                for c in [col, col - 1]:
                    if matrix[row, c] == -1:  # Aquí cambias el 0 por -1
                        try:
                            bit = next(bit_iter)
                            matrix[row, c] = int(bit)
                        except StopIteration:
                            return matrix

            # Switch vertical direction for the next column pair
            going_up = not going_up
            col -= 2

        return matrix


    def final_matrix_output(self) -> np.ndarray:
        self.encode_string_text()
        matrix = self.format_matrix()
        final_bits = self.ger_ec_codewords()
        mat = self.place_qr_data_bits(matrix, final_bits)
        mat, mask_id = self.select_best_mask(mat, matrix)
        return mat



