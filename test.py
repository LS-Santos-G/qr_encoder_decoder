mode_indicator = '0100'
char_count_indicator = '' #debe ser de 8 bits

def hello(message):
    databits = ''
    for ch in message:
        ch_byte = bin(ord(ch))[2:]
        while len(ch_byte) < 8:
            ch_byte = '0' + ch_byte
        databits += ch_byte
    print(databits)

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
print(qr_specs['M']['max_num_bits'])