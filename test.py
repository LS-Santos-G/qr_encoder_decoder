mode_indicator = '0100'
char_count_indicator = '' #debe ser de 8 bits

unencoded_text = '' #ingresado por el usuario

def encode_text_bin(text: str):
    text_list = list(text)
    print(text_list)

    hex_list = []
    for let in text_list:
        hex_list.append(let.encode("utf-8").hex())

    print(hex_list)

encode_text_bin('hhg')
