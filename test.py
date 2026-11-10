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

hello('HHH')