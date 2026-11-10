from enum import Enum



#nivel de correccion
class ErrorCorrection(Enum):
    LOW = 'L'
    MID = 'M'
    QTR = 'Q'
    HIG = 'H'

class Encoder:
    def __init__(self, message: str, error_correction: ErrorCorrection):
        self.message = message
        self.error_correction = error_correction

    #numero de bits del qr
    def set_max_num_bits(self, error_corr: ErrorCorrection):
        match error_corr:
            case ErrorCorrection.LOW:
                return  8*194
            case ErrorCorrection.MID:
                return 8*154
            case ErrorCorrection.QTR:
                return 8*110
            case ErrorCorrection.HIG:
                return 8*86

    #largo del texto como numero binario de 8 bits
    def encode_string(self):
        # modo byte
        mode_indicator = '0100'
        # len del mensaje en binario, 8 bits
        char_count_indicator = f"{len(self.message):08b}"
        # depende del tipo de correcion escogida
        max_num_bits = self.set_max_num_bits(self.error_correction)
        #mensaje en binario, cada char de 8 bits
        messsage_binary = "".join([f"{ord(char):08b}" for char in self.message])

        #junta los strings anteriores
        encoded_message = mode_indicator + char_count_indicator + messsage_binary
        #cadenas faltantes

        #agrega los bits terminales necesarios
        if len(encoded_message) > max_num_bits:  # PON ALGO EN LA INTERFAZ
            print('No se puede!')
            return
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
