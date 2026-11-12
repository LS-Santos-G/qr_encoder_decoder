from enum import Enum

#nivel de correccion
class ErrorCorrection(Enum):
    LOW = 'L'
    MID = 'M'
    QTR = 'Q'
    HIG = 'H'

class Encoder:
    #caracteristica universal de cada encoder
    qr_specs = {
    'L': {
        'ec_per_block': 24,
        'groups': [
            {'num_blocks': 2, 'data_per_block': 97} ],
        'max_num_bits': 8*194
    },
    'M': {
        'ec_per_block': 22,
        'groups': [
            {'num_blocks': 2, 'data_per_block': 38},
            {'num_blocks': 2, 'data_per_block': 39}],
        'max_num_bits': 8*154
    },
    'Q': {
        'ec_per_block': 22,
        'groups': [
            {'num_blocks': 4, 'data_per_block': 18},
            {'num_blocks': 2, 'data_per_block': 19}],
        'max_num_bits': 8*110
    },
    'H': {
        'ec_per_block': 26,
        'groups': [
            {'num_blocks': 4, 'data_per_block': 14},
            {'num_blocks': 2, 'data_per_block': 15} ],
        'max_num_bits': 8*86
    }
}
    def __init__(self, message: str, error_correction: str):
        #mensaje
        self.message = message
        #correcion seleccionada
        self.error_correction = error_correction

    #largo del texto como numero binario de 8 bits
    def encode_string_text(self):
        # modo byte
        mode_indicator = '0100'
        # len del mensaje en binario, 8 bits
        char_count_indicator = f"{len(self.message):08b}"
        # numero de bits maximo, depende del tipo de correcion escogida
        max_num_bits = Encoder.qr_specs[self.error_correction]['max_num_bits']
        #mensaje en binario, cada char de 8 bits
        messsage_binary = "".join([f"{ord(char):08b}" for char in self.message])

        #junta los strings anteriores
        encoded_message = mode_indicator + char_count_indicator + messsage_binary

        #cadenas faltantes

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
            repeats = (difference + len(pad_bytes) - 1) // len(pad_bytes)

            padding = (pad_bytes * repeats)[:needed]

            encoded_message += padding

        return encoded_message
