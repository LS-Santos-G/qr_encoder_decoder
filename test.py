import numpy as np
import matplotlib.pyplot as plt

qr_size = (((1-1)*4)+21)

matrix = np.zeros((qr_size, qr_size))


def draw_finder_pattern(matrixn, row_start, col_start):
    for i in range(7):
        for j in range(7):
            # Determine if the current module should be black (1) or white (0)
            # Outer border (i=0,6 or j=0,6) or inner block (2 <= i,j <= 4)
            is_outer = (i == 0 or i == 6 or j == 0 or j == 6)
            is_inner = (2 <= i <= 4 and 2 <= j <= 4)

            if is_outer or is_inner:
                matrixn[row_start + i, col_start + j] = 1
            else:
                matrixn[row_start + i, col_start + j] = 0
def draw_timing_patterns(matrix):
    for i in range(8, 13,2):
        matrix[i][6] = 1
        matrix[6][i] = 1
draw_finder_pattern(matrix, 0, 0)
draw_finder_pattern(matrix, 0, 14)
draw_finder_pattern(matrix, 14, 0)
draw_timing_patterns(matrix)
matrix[4+9][8] = 1
plt.imshow(matrix, cmap='gray_r')
plt.show()