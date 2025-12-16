import math
import numpy as np


def determinant(matrix):
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    if n == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    det = 0.0
    for j in range(n):
        minor = [[matrix[i][k] for k in range(n) if k != j] for i in range(1, n)]
        det += ((-1) ** j) * matrix[0][j] * determinant(minor)
    return det


def inverse_matrix(matrix):
    M = [[float(x) for x in row] for row in matrix]
    n = len(M)
    det = determinant(M)
    if abs(det) < 1e-14:
        raise ValueError("Матрица вырождена")

    adj = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            minor = []
            for ii in range(n):
                if ii == i:
                    continue
                row = []
                for jj in range(n):
                    if jj == j:
                        continue
                    row.append(M[ii][jj])
                minor.append(row)
            cofactor = ((-1) ** (i + j)) * determinant(minor)
            adj[j][i] = cofactor

    return [[adj[i][j] / det for j in range(n)] for i in range(n)]


def F_vec(x):
    xv, yv, zv = x
    f1 = xv + xv * xv - 2 * yv * zv - 0.1
    f2 = yv - yv * yv + 3 * xv * zv + 0.2
    f3 = zv + zv * zv + 2 * xv * yv - 0.3
    return [f1, f2, f3]


def J_mat(x):
    xv, yv, zv = x
    j11 = 1 + 2 * xv
    j12 = -2 * zv
    j13 = -2 * yv
    j21 = 3 * zv
    j22 = 1 - 2 * yv
    j23 = 3 * xv
    j31 = 2 * yv
    j32 = 2 * xv
    j33 = 1 + 2 * zv
    return [[j11, j12, j13],
            [j21, j22, j23],
            [j31, j32, j33]]


def Phi(x):
    F = F_vec(x)
    return 0.5 * sum(fi * fi for fi in F)


def norm(v):
    return math.sqrt(sum(vi * vi for vi in v))


# =============================
# Метод Зейделя
# =============================
def seidel_method(x0, eps=1e-3, max_iter=500):
    x, y, z = x0

    # Проверка достаточного условия сходимости
    J_phi = [
        [-2 * x0[0], 2 * x0[1], 2 * x0[2]],
        [-3 * x0[2], 2 * x0[1], -3 * x0[0]],
        [-2 * x0[1], -2 * x0[0], -2 * x0[2]]
    ]
    row_sums = [sum(abs(v) for v in row) for row in J_phi]
    max_norm = max(row_sums)
    if max_norm >= 1:
        print(f"Достаточное условие сходимости метода Зейделя не выполняется {max_norm:.4f}")
    else:
        print(f"Достаточное условие сходимости выполнено {max_norm:.4f}")

    history = []
    for k in range(max_iter):
        x_old, y_old, z_old = x, y, z
        x = 0.1 - x_old * x_old + 2 * y_old * z_old
        y = -0.2 + y_old * y_old - 3 * x * z_old
        z = 0.3 - z_old * z_old - 2 * x * y
        Fx = F_vec([x, y, z])
        res = norm(Fx)
        history.append((k, [x, y, z], Fx, res))

        delta = max(abs(x - x_old), abs(y - y_old), abs(z - z_old))
        if delta < eps:
            break

    return [x, y, z], history


# =============================
# Метод Ньютона
# =============================
def matrix_vector_mul(A, v):
    return [sum(A[i][j] * v[j] for j in range(3)) for i in range(3)]


def vector_sub(a, b):
    return [a[i] - b[i] for i in range(3)]


def newton_method(x0, eps_x=1e-6, max_iter=50):
    x = x0[:]
    hist = []
    last_invJ = None

    for k in range(max_iter):
        x_old = x[:]
        Fv = F_vec(x)
        F_norm = norm(Fv)
        J = J_mat(x)
        try:
            invJ = inverse_matrix(J)
        except:
            print(f"Ошибка обращения матрицы на итерации {k}")
            break

        last_invJ = invJ
        hist.append((k, x[:], Fv[:], F_norm))

        dx = matrix_vector_mul(invJ, Fv)
        x = vector_sub(x, dx)

        delta = max(abs(x[i] - x_old[i]) for i in range(3))
        if delta < eps_x:
            break

    return x, hist, last_invJ


if __name__ == "__main__":
    x0 = [0.1, -0.1, 0.1]

    # --- Метод Зейделя ---
    x_seid, hist_seid = seidel_method(x0)
    kS, xS, F_seid_vec, resS = hist_seid[-1]

    print("Метод Зейделя")
    print("Количество итераций =", kS + 1)
    print("x:")
    for v in x_seid:
        print(f"{v:.4f}")
    print("\nВектор невязки F(x):")
    for val in F_seid_vec:
        print(f"{val:.16f}")
    print("Норма невязки =", f"{resS:.16f}")
    print("Phi =", f"{Phi(x_seid):.16f}")
    print()

    # --- Метод Ньютона ---
    x_newt, hist_newt, last_inv = newton_method(x_seid)
    kN, xN, F_newt_vec, resN = hist_newt[-1]

    print("Метод Ньютона")
    print("Количество итераций =", len(hist_newt))
    print("x:")
    for v in x_newt:
        print(f"{v:.4f}")
    print("\nВектор невязки F(x):")
    for val in F_newt_vec:
        print(f"{val:.16f}")
    print("Норма невязки =", f"{resN:.16f}")
    print("Phi =", f"{Phi(x_newt):.16f}")

    print("\nОбратная матрица Якоби (в точке решения):")
    if last_inv is not None:
        for row in last_inv:
            print("  ".join(f"{val:.4f}" for val in row))
    else:
        print("Не вычислена")

    # --- NumPy проверка ---
    print("\nNumPy проверка:")
    F_np = np.array(F_vec(x_newt))
    print("Вектор невязки:")
    for val in F_np:
        print(f"{val:.16f}")
    print(f'Норма = {np.linalg.norm(F_np):.16f}')
