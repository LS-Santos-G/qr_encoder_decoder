from encoder import Encoder

import numpy as np
import matplotlib.pyplot as plt
from encoder import Encoder


def place_qr_data_bits(matrix: np.ndarray, encoded_bits: str) -> np.ndarray:
    #copy to avoid mutating the original array in-place unexpectedly
    matrix = matrix.copy()
    size = matrix.shape[0]
    bit_iter = iter(encoded_bits)

    # QR code bit placement starts from the bottom-right corner
    col = size - 1
    going_up = True

    while col > 0:
        
        # Column 6 is reserved for the vertical timing pattern; skip it and shift to column 5
        if col == 6:
            col -= 1

        # Determine row traversal direction based on the zigzag pattern
        row_range = range(size - 1, -1, -1) if going_up else range(0, size)

        for row in row_range:
            # Process the two columns in the current pair (right column first, then left column)
            for c in [col, col - 1]:
                # Only insert a bit if the cell is designated for data (initialized to 0)
                if matrix[row, c] == 0:
                    try:
                        bit = next(bit_iter)
                        matrix[row, c] = int(bit)
                    except StopIteration:
                        # Ran out of bits to place
                        return matrix

        # Switch vertical direction for the next column pair
        going_up = not going_up
        col -= 2

    return matrix
test = Encoder('apple', 'L')
test.encode_string_text()
matrix = test.format_matrix()


mat =  place_qr_data_bits(matrix, test.encoded_message)
for row in mat:
    print(row)
plt.imshow(mat, cmap='gray_r')
plt.show()
