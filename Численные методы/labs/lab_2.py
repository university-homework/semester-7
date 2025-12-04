# вариант 11 (Г)
# прямой: метод вращения (В) (Амосов Дубинский с.165)
# итерационный: метод минимальных невязок (Д) (Самарский, Гулин, с.116)


from math import sqrt, floor
from copy import deepcopy, copy

import numpy as np


class Printer:
    @staticmethod
    def first_order_matrix(array, name):
        print(f'{name}:')
        for item in array:
            print(f"{item:.4f}")

    @staticmethod
    def second_order_matrix(array, name):
        print(f'{name}:')
        for row in array:
            print("  ".join(f"{item:.4f}" for item in row))

    @staticmethod
    def residual(array):
        print(f"\nНевязка:")
        for item in array:
            print(f"{item:.16f}")


def mn(A):
    n = len(A)
    max_sum = 0
    for j in range(n):
        col_sum = sum(abs(A[i][j]) for i in range(n))
        if col_sum > max_sum:
            max_sum = col_sum
    return max_sum


def scalar_product(x, y):
    return sum(x_i * y_i for x_i, y_i in zip(x, y))


def method_rotations(A, f):
    n = len(A)

    for i in range(n - 1):
        for j in range(i + 1, n):
            if abs(A[j][i]) < 1e-6:
                continue

            r = sqrt(A[i][i] ** 2 + A[j][i] ** 2)
            c = A[i][i] / r
            s = A[j][i] / r

            for k in range(i, n):
                temp_i = A[i][k]
                temp_j = A[j][k]
                A[i][k] = c * temp_i + s * temp_j
                A[j][k] = -s * temp_i + c * temp_j

            temp_f_i = f[i]
            temp_f_j = f[j]
            f[i] = c * temp_f_i + s * temp_f_j
            f[j] = -s * temp_f_i + c * temp_f_j

    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        s = f[i]
        for j in range(i + 1, n):
            s -= A[i][j] * x[j]
        x[i] = s / A[i][i]

    return x


def method_minimal_residuals(A, f, x0, eps):
    n = len(A)
    x_prev = x0.copy()
    k = 0

    while True:
        # Вычисляем невязку
        r_prev = residual(A, x_prev, f)

        # Вычисляем A * r_prev
        A_r = [0.0] * n
        for i in range(n):
            s = 0.0
            for j in range(n):
                s += A[i][j] * r_prev[j]
            A_r[i] = s

        # Вычисляем оптимальный параметр τ
        numerator = scalar_product(r_prev, A_r)
        denominator = scalar_product(A_r, A_r)

        if abs(denominator) < eps:
            break

        tau = numerator / denominator

        # Новая итерация
        x_new = [x_prev[i] - tau * r_prev[i] for i in range(n)]

        # Проверка условия остановки
        diff = [x_new[i] - x_prev[i] for i in range(n)]
        norm_diff = sqrt(sum(x_i ** 2 for x_i in diff))

        if norm_diff < eps:
            break

        x_prev = x_new.copy()
        k += 1

        # Защита от бесконечного цикла
        if k > 10000:
            break

    return x_new, k


def gauss(A, f):
    n = len(f)
    for i in range(n):
        max_row = i
        for k in range(i + 1, n):
            if abs(A[k][i]) > abs(A[max_row][i]):
                max_row = k

        if max_row != i:
            A[i], A[max_row] = A[max_row], A[i]
            f[i], f[max_row] = f[max_row], f[i]

        for j in range(i + 1, n):
            factor = A[j][i] / A[i][i]
            for k in range(i, n):
                A[j][k] -= factor * A[i][k]
            f[j] -= factor * f[i]

    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = f[i]
        for j in range(i + 1, n):
            x[i] -= A[i][j] * x[j]
        x[i] /= A[i][i]

    return x


def inverse(A):
    n = len(A)
    inv = [[0] * n for _ in range(n)]

    for i in range(n):
        e = [0] * n
        e[i] = 1
        col = gauss([row[:] for row in A], e)
        for j in range(n):
            inv[j][i] = col[j]

    return inv


def residual(A, x, f):
    n = len(A)
    r = [0.0] * n
    for i in range(n):
        s = 0.0
        for j in range(n):
            s += A[i][j] * x[j]
        r[i] = s - f[i]
    return r


def condition_number(A):
    norm_A = mn(A)
    A_inv = inverse(A)
    norm_A_inv = mn(A_inv)
    M_A = norm_A * norm_A_inv
    return M_A


def main(printer):
    A = [
        [12.00, -3.00, -1.00, 3.00],
        [-3.00, 15.00, 5.00, -5.00],
        [-1.00, 5.00, 10.00, 2.00],
        [3.00, -5.00, 2.00, 11.00]
    ]
    b = [-26.00, -55.00, -58.00, -24.00]
    eps = 1e-6

    printer.second_order_matrix(A, 'A')
    printer.first_order_matrix(b, '\nb')

    print(f"\nМЕТОД ВРАЩЕНИЙ")
    print('-' * 60)

    x = method_rotations(deepcopy(A), copy(b))
    r = residual(A, x, b)

    printer.first_order_matrix(x, 'x')
    printer.residual(r)
    print('-' * 60)

    print(f"\nМЕТОД МИНИМАЛЬНЫХ НЕВЯЗОК")
    print('-' * 60)

    x0 = [floor(val) for val in x]
    x2, k2 = method_minimal_residuals(deepcopy(A), copy(b), x0, eps)
    r2 = residual(A, x2, b)

    printer.first_order_matrix(x0, '\nНачальное приближение')
    printer.first_order_matrix(x2, '\nx')
    printer.residual(r2)
    print(f"Метод сошелся за {k2} итераций(ю)")
    print('-' * 60)

    M_A = condition_number(A)
    print(f"\nЧисло обусловленности (numpy): {np.linalg.cond(A, 1):.4f}")
    print(f"Число обусловленности (наше вычисление): M = {M_A:.4f}")


if __name__ == '__main__':
    main(Printer())
