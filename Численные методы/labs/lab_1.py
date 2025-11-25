from copy import deepcopy, copy

import numpy


class LinearAlgebraSolver:
    @staticmethod
    def gauss_elimination(A: list[list[float]], f: list[float]) -> list[float]:
        """Решение СЛАУ методом Гаусса с частичным выбором ведущего элемента"""
        n = len(f)
        A = deepcopy(A)
        f_copy = copy(f)

        # Прямой ход
        for i in range(n):
            # Выбор ведущего элемента
            max_row = i
            for k in range(i + 1, n):
                if abs(A[k][i]) > abs(A[max_row][i]):
                    max_row = k

            # Перестановка строк
            if max_row != i:
                A[i], A[max_row] = A[max_row], A[i]
                f_copy[i], f_copy[max_row] = f_copy[max_row], f_copy[i]

            # Исключение переменной
            for j in range(i + 1, n):
                factor = A[j][i] / A[i][i]
                for k in range(i, n):
                    A[j][k] -= factor * A[i][k]
                f_copy[j] -= factor * f_copy[i]

        # Обратный ход
        x = [0.0] * n
        for i in range(n - 1, -1, -1):
            x[i] = f_copy[i]
            for j in range(i + 1, n):
                x[i] -= A[i][j] * x[j]
            x[i] /= A[i][i]

        return x

    @staticmethod
    def determinant(A: list[list[float]]) -> float:
        """Вычисление определителя матрицы методом Гаусса"""
        n = len(A)
        A_copy = [row[:] for row in A]
        det_value = 1.0

        for i in range(n):
            # Выбор ведущего элемента
            max_row = i
            for k in range(i + 1, n):
                if abs(A_copy[k][i]) > abs(A_copy[max_row][i]):
                    max_row = k

            # Перестановка строк
            if max_row != i:
                A_copy[i], A_copy[max_row] = A_copy[max_row], A_copy[i]
                det_value *= -1

            # Проверка на вырожденность
            if abs(A_copy[i][i]) < 1e-12:
                return 0.0

            det_value *= A_copy[i][i]

            # Исключение
            for j in range(i + 1, n):
                factor = A_copy[j][i] / A_copy[i][i]
                for k in range(i + 1, n):
                    A_copy[j][k] -= factor * A_copy[i][k]

        return det_value

    @staticmethod
    def inverse_matrix(A: list[list[float]]) -> list[list[float]]:
        """Вычисление обратной матрицы методом Гаусса"""
        n = len(A)
        inv = [[0] * n for _ in range(n)]
        # Решаем систему для каждого столбца единичной матрицы
        for i in range(n):
            e = [0.0] * n
            e[i] = 1.0
            col = LinearAlgebraSolver.gauss_elimination([row[:] for row in A], e)
            for j in range(n):
                inv[j][i] = col[j]

        return inv

    @staticmethod
    def matrix_vector_multiply(A: list[list[float]], x: list[float]) -> list[float]:
        """Умножение матрицы на вектор"""
        n = len(A)
        result = [0.0] * n
        for i in range(n):
            for j in range(n):
                result[i] += A[i][j] * x[j]
        return result

    @staticmethod
    def matrix_multiply(A: list[list[float]], B: list[list[float]]) -> list[list[float]]:
        """Умножение матриц"""
        n = len(A)
        C = [[0.0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    @staticmethod
    def residual_vector(A: list[list[float]], x: list[float], f: list[float]) -> list[float]:
        """Вычисление вектора невязки r = A*x - f"""
        r = LinearAlgebraSolver.matrix_vector_multiply(A, x)
        for i in range(len(r)):
            r[i] -= f[i]
        return r


class MatrixFormatter:
    @staticmethod
    def format_matrix(matrix: list[list[float]], precision: int = 4) -> list[list[str]]:
        """Форматирование матрицы для красивого вывода"""
        return [[f"{val:.{precision}f}" for val in row] for row in matrix]

    @staticmethod
    def format_vector(vector: list[float], precision: int = 4) -> list[str]:
        """Форматирование вектора для красивого вывода"""
        return [f"{val:.{precision}f}" for val in vector]

    @staticmethod
    def print_matrix(matrix: list[list[float]], name: str = "", precision: int = 4):
        """Печать матрицы с заголовком"""
        if name:
            print(f"{name} =")
        formatted = MatrixFormatter.format_matrix(matrix, precision)
        for row in formatted:
            print('  '.join(row))

    @staticmethod
    def print_vector(vector: list[float], name: str = "", precision: int = 4):
        """Печать вектора с заголовком"""
        if name:
            print(f"{name} =")
        formatted = MatrixFormatter.format_vector(vector, precision)
        print('\n'.join(formatted))


def main():
    # Исходные данные
    A = [
        [1.28, 0.42, 0.54, 1.00],
        [2.11, 3.01, 4.02, 0.22],
        [0.18, 3.41, 0.15, 1.43],
        [2.14, 0.17, 0.26, 0.18]
    ]
    f = [1.34, 1.56, 1.78, 1.91]

    solver = LinearAlgebraSolver()
    formatter = MatrixFormatter()

    # Вывод исходных данных
    formatter.print_matrix(A, "Матрица A", 2)
    formatter.print_vector(f, "Вектор f", 2)

    # Решение системы
    x = solver.gauss_elimination(A, f)

    print("\nРешение системы:")
    for i, val in enumerate(x):
        print(f"  x{i + 1} = {val:.4f}")

    # Вектор невязки
    r = solver.residual_vector(A, x, f)
    print("\nВектор невязки:")
    for i, val in enumerate(r):
        print(f"  r{i + 1} = {val:.16f}")

    # Определитель
    det_value = solver.determinant(A)
    print(f"\nОпределитель det(A) = {det_value:.4f}")

    A_np = numpy.array(A)
    det_numpy = numpy.linalg.det(A_np)
    print(f"Определитель через numpy = {det_numpy:.4f}")

    # Обратная матрица
    A_inv = solver.inverse_matrix(A)
    formatter.print_matrix(A_inv, "\nОбратная матрица A^-1", 4)

    # Проверка A * A^(-1) = E
    E = solver.matrix_multiply(A, A_inv)
    formatter.print_matrix(E, "\nПроверка A * A^-1 (должна быть единичная матрица)", 2)


if __name__ == "__main__":
    main()
