import numpy as np
from matplotlib import pyplot as plt
from reedsolo import RSCodec

#qr ver 2
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
    def __init__(self, message: str, error_correction: str):
        #mensaje
        self.message = message
        #correcion seleccionada
        self.error_correction = qr_specs[error_correction]
        self.level = error_correction
        self.encoded_message = ''

    #largo del texto como numero binario de 8 bits
    def encode_string_text(self):
        mode_indicator = '0100' # modo byte

        if(len(self.message) > self.error_correction['char_capacity']):
            print('El mensaje es muy largo para este nivel!')
            return -1

        char_count_indicator = f"{len(self.message):08b}"  # len del mensaje en binario, 8 bits
        messsage_binary = "".join(
        [f"{ord(char):08b}" for char in self.message])  # mensaje en binario, cada char de 8 bits

        #junta los strings anteriores
        encoded_message = mode_indicator + char_count_indicator + messsage_binary

        #cadenas faltantes
        max_num_bits = self.error_correction['max_num_bits']  # numero de bits maximo,

        #agrega los bits terminales necesarios
        if len(encoded_message) > max_num_bits:  # PON ALGO EN LA INTERFAZ
            print('No se puede!')
            return -1
        else:
            difference = max_num_bits - len(encoded_message)
            if difference > 4:
                encoded_message += '0'*4
            else:
                encoded_message += '0' * difference

        #hace que el largo del string sea multiplo de 8
        r = len(encoded_message) % 8
        if r != 0:
            encoded_message += '0'*(8-r)

        #llena la string hasta llegar al maximo permitido
        if len(encoded_message) != max_num_bits:
            needed = max_num_bits - len(encoded_message)
            pad_bytes = '1110110000010001'
            repeats = (needed + len(pad_bytes) - 1) // len(pad_bytes)

            padding = (pad_bytes * repeats)[:needed]

            encoded_message += padding

        self.encoded_message = encoded_message
        return 1

    def ger_ec_codewords(self, encoded_message):
        encoded_message = self.encoded_message #mensaje

        ec_per_block = self.error_correction['ec_per_block'] #num palabras correccion

        # reed solomon del bloque
        rs = RSCodec(ec_per_block)

        # retorna las ec del bloque
        encoded_with_ecs = rs.encode(bytes(int(encoded_message[i:i+8], 2) for i in range(0, len(encoded_message), 8)))

        return encoded_with_ecs

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
        bits = "".join(f"{byte:08b}" for byte in self.ger_ec_codewords(self.encoded_message))
        bit_iter = iter(bits)
        col = 20
        going_up = True
        while col > 0:
            if col == 6:
                col -= 1
            for row in (range(20, -1, -1) if going_up else range(21)):
                for c in [col, col - 1]:
                    if not self.reserved[row, c]:
                        matrix[row, c] = int(next(bit_iter)) ^ ((row + c) % 2 == 0)
            going_up = not going_up
            col -= 2
        return matrix

    def draw_format_info(self, matrix):
        data = ({'L': 1, 'M': 0, 'Q': 3, 'H': 2}[self.level] << 3) | 0
        rem = data << 10
        for i in range(14, 9, -1):
            if (rem >> i) & 1:
                rem ^= 0x537 << (i - 10)
        word = ((data << 10) | rem) ^ 0x5412
        bit = lambda i: (word >> i) & 1

        for i in range(6):
            matrix[i][8] = bit(i)
        matrix[7][8] = bit(6)
        matrix[8][8] = bit(7)
        matrix[8][7] = bit(8)
        for i in range(9, 15):
            matrix[8][14 - i] = bit(i)

        for i in range(8):
            matrix[8][20 - i] = bit(i)
        for i in range(8, 15):
            matrix[6 + i][8] = bit(i)

    def build_matrix(self):
        matrix = self.format_matrix()
        self.place_data(matrix)
        self.draw_format_info(matrix)
        return matrix
    def format_matrix(self):
        matrix = np.zeros([21, 21])
        self.reserved = np.zeros([21, 21], dtype=bool)
        self.reserved[:9, :9] = self.reserved[:9, 13:] = self.reserved[13:, :9] = True
        self.reserved[6, :] = self.reserved[:, 6] = True

        #los cuadrados de las ezquinas
        self.draw_finder_pattern(matrix, 0, 0)
        self.draw_finder_pattern(matrix, 0, 14)
        self.draw_finder_pattern(matrix, 14, 0)

        self.draw_timing_patterns(matrix) #las rayas

        #puntico (dark module)
        matrix[4+9][8] = 1

        return matrix
    #pone la información tras poner el formato
