import numpy as np


def bsc(matrix: np.ndarray, p: float, rng=None) -> np.ndarray:
   #cada módulo se invierte con probabilidad p, de forma independiente y afecta a todo el símbolo 
    rng = rng or np.random.default_rng()
    flips = rng.random(matrix.shape) < p
    return np.bitwise_xor(matrix.astype(int), flips.astype(int))


def flip_exact(matrix: np.ndarray, fraction: float, rng=None) -> np.ndarray:
   # para reportar el porcentaje de daño sin la varianza del BSC
    rng = rng or np.random.default_rng()
    out = matrix.astype(int).copy().ravel()
    k = round(fraction * out.size)
    idx = rng.choice(out.size, size=k, replace=False)
    out[idx] ^= 1
    return out.reshape(matrix.shape)


def burst(matrix: np.ndarray, fraction: float, rng=None, mode="invert") -> np.ndarray:
    rng = rng or np.random.default_rng()
    out = matrix.astype(int).copy()
    n = out.shape[0]
    area = round(fraction * n * n)
    if area == 0:
        return out
    h = min(n, max(1, int(round(np.sqrt(area)))))
    w = min(n, max(1, int(np.ceil(area / h))))
    r0 = rng.integers(0, n - h + 1)
    c0 = rng.integers(0, n - w + 1)
    patch = out[r0:r0 + h, c0:c0 + w]
    out[r0:r0 + h, c0:c0 + w] = (patch ^ 1) if mode == "invert" else 0
    return out
