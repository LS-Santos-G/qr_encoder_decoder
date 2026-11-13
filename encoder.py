from reedsolo import RSCodec

#qr ver 2
qr_specs = {
    'L': {
        'ec_per_block': 10,
        'char_capacity':32,
        'max_num_bits': 8*34
    },
    'M': {
        'ec_per_block': 16,
        'char_capacity':26,
        'max_num_bits': 8*28
    },
    'Q': {
        'ec_per_block': 22,
        'char_capacity':20,
        'max_num_bits': 8*22
    },
    'H': {
        'ec_per_block': 28,
        'char_capacity': 14,
        'max_num_bits': 8*16
    }
}
class Encoder:
    def __init__(self, message: str, error_correction: str):
        #mensaje
        self.message = message
        #correcion seleccionada
        self.error_correction = qr_specs[error_correction]
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
        encoded_with_ecs = rs.encode(encoded_message)


    


