import numpy as np


def is_matrix_rgb(matrix: np.ndarray) -> bool:
    return len(matrix.shape) > 2
