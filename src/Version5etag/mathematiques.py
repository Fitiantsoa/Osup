import numpy as np


class Mathematique:
    def __init__(self, matrix=None, vector=None):
        self._matrix = matrix
        self._vector = vector
        self._size = len(self._vector)

    def magnitude(self):
        vabs = np.zeros((self._size, 1))
        for i in range(self._size):
            vabs[i, 0] = abs(self._vector[i])
        magnitude = vabs[0, 0]
        for i in range(self._size - 1):
            if vabs[i + 1, 0] >= magnitude:
                magnitude = vabs[i + 1, 0]
        return magnitude

    def product_matrix_vector(self):
        product = np.zeros((self._size, 1))
        for i in range(self._size):
            for j in range(self._size):
                product[i, 0] = product[i, 0] + self._matrix[i, j] * self._vector[j]
        return product
