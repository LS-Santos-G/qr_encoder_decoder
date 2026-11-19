import numpy as np
from reedsolo import RSCodec, ReedSolomonError

EC = {"L": 7, "M": 10, "Q": 13, "H": 17}
LEVEL_BITS = {"L": 1, "M": 0, "Q": 3, "H": 2}

MASKS = [
    lambda i, j: (i + j) % 2 == 0,
    lambda i, j: i % 2 == 0,
    lambda i, j: j % 3 == 0,
    lambda i, j: (i + j) % 3 == 0,
    lambda i, j: (i // 2 + j // 3) % 2 == 0,
    lambda i, j: (i * j) % 2 + (i * j) % 3 == 0,
    lambda i, j: ((i * j) % 2 + (i * j) % 3) % 2 == 0,
    lambda i, j: ((i + j) % 2 + (i * j) % 3) % 2 == 0,
]

RESERVED = np.zeros((21, 21), dtype=bool)
RESERVED[:9, :9] = RESERVED[:9, 13:] = RESERVED[13:, :9] = True
RESERVED[6, :] = RESERVED[:, 6] = True


def format_word(data):
    rem = data << 10
    for i in range(14, 9, -1):
        if (rem >> i) & 1:
            rem ^= 0x537 << (i - 10)
    return ((data << 10) | rem) ^ 0x5412


FORMATS = {format_word((LEVEL_BITS[l] << 3) | k): (l, k) for l in EC for k in range(8)}


def read_format(m):
    copy1 = [m[i][8] for i in range(6)] + [m[7][8], m[8][8], m[8][7]] + [m[8][14 - i] for i in range(9, 15)]
    copy2 = [m[8][20 - i] for i in range(8)] + [m[6 + i][8] for i in range(8, 15)]
    best = (99, None)
    for copy in (copy1, copy2):
        word = sum(int(b) << i for i, b in enumerate(copy))
        for valid, info in FORMATS.items():
            best = min(best, (bin(word ^ valid).count("1"), info), key=lambda t: t[0])
    return best[1] if best[0] <= 3 else None


def decode_matrix(m):
    m = np.array(m, dtype=int)
    info = read_format(m)
    if info is None:
        return None
    level, mask = info

    bits = []
    col, up = 20, True
    while col > 0:
        if col == 6:
            col -= 1
        for r in (range(20, -1, -1) if up else range(21)):
            for c in (col, col - 1):
                if not RESERVED[r, c]:
                    bits.append(m[r, c] ^ int(MASKS[mask](r, c)))
        up = not up
        col -= 2
    raw = bytes(int("".join(map(str, bits[i:i + 8])), 2) for i in range(0, 208, 8))

    try:
        data = bytes(RSCodec(EC[level]).decode(bytearray(raw))[0])
    except ReedSolomonError:
        return None

    bits = "".join(f"{b:08b}" for b in data)
    n = int(bits[4:12], 2)
    if bits[:4] != "0100" or 12 + 8 * n > len(bits):
        return None
    return bytes(int(bits[12 + 8 * k:20 + 8 * k], 2) for k in range(n)).decode("latin-1")
