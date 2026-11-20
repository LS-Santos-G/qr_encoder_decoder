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
            for c in [col, col - 1]:
                if matrix[row, c] == -1:  # Aquí cambias el 0 por -1
                    try:
                        bit = next(bit_iter)
                        matrix[row, c] = int(bit)
                    except StopIteration:
                        return matrix

        # Switch vertical direction for the next column pair
        going_up = not going_up
        col -= 2

    return matrix


test = Encoder('Caracol', 'L')
test.encode_string_text()
matrix = test.format_matrix()

final_bits = test.ger_ec_codewords()
mat = place_qr_data_bits(matrix, final_bits)
mat, mask_id = test.select_best_mask(mat, matrix)

print("Máscara elegida:", mask_id)
print("Penalización:", test.calculate_penalty(mat))

plt.imshow(
    mat == 1,
    cmap="gray_r",
    vmin=0,
    vmax=1,
    interpolation="nearest"
)
plt.show()