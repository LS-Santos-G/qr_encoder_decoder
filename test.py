encoded_message = "00001111"

needed = 32 - len(encoded_message)
pad_bytes = '11101100 00010001'
repeats = (needed + len(pad_bytes) - 1) // len(pad_bytes)

padding = (pad_bytes * repeats)[:needed]

encoded_message += padding

print(encoded_message)
11101100 00010001 11101100