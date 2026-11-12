from reedsolo import RSCodec


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
class Encoder:
    def __init__(self, message: str, error_correction: str):
        #mensaje
        self.message = message
        #correcion seleccionada
        self.error_correction = qr_specs[error_correction]
        self.encoded_message = ''

    #largo del texto como numero binario de 8 bits
    def encode_string_text(self):
        # modo byte
        mode_indicator = '0100'
        # len del mensaje en binario, 8 bits
        char_count_indicator = f"{len(self.message):08b}"
        # numero de bits maximo, depende del tipo de correcion escogida
        max_num_bits = self.error_correction['max_num_bits']
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

        self.encoded_message = encoded_message
        return 1

    #separa el mensaje en bloques segun la version
    def separate_blocks(self, message_bytes: bytes) -> bytes:
        ec_per_block = self.error_correction['ec_per_block']
        message_bytes = bytes(self.encoded_message, 'utf-8')
        all_blocks = []
        current_index = 0

        for group in self.error_correction['groups']:
            num_blocks = group['num_blocks']  # num bloques por grupo
            data_per_block = group['data_per_block']  # num parabras por bloque
            for _ in range(num_blocks):
                block_data = message_bytes[current_index: current_index + data_per_block]
                if len(block_data) < data_per_block:
                    raise ValueError("EL MENSAJE ES MUY CORTO PARA ESTE TIPO DE QR")
                all_blocks.append(block_data)
                current_index += data_per_block

        return all_blocks

    def ger_ec_codewords(self, encoded_message):

            all_blocks = self.separate_blocks(encoded_message)
            num_blocks = len(all_blocks)
            ec_per_block = self.error_correction['ec_per_block'] #num palabras correccion
            #guarda las palabras de corrección de todos los bloques
            all_ec_codewords = []

            for index in range(num_blocks):
                #el bloque actual
                target_block = all_blocks[index]

                # reed solomon del bloque
                rs = RSCodec(ec_per_block)

                # retorna las ec del bloque
                encoded = rs.encode(target_block)
                ec_codewords = encoded[len(target_block):]

                all_ec_codewords.append(ec_codewords)

            return all_ec_codewords

    def interweave_words(self):
        all_blocks = self.separate_blocks(self.encoded_message)
        interweaved_words = ''


