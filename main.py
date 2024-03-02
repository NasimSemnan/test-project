import numpy as np


def create_matrix(rows: int, cols: int):
    return np.zeros((rows, cols))


print(create_matrix(12, 5))
