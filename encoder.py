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

        #los cuadrados de las ezquinas
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
