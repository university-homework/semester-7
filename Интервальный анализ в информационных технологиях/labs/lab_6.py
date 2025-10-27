import math
import numpy as np


def solve_tridiagonal_interval(V, M):
    Rad = 0.01

    # Создаем массивы для интервальных коэффициентов (индексация 1..M)
    A_l = np.zeros(M + 2)
    A_r = np.zeros(M + 2)
    B_l = np.zeros(M + 2)
    B_r = np.zeros(M + 2)
    C_l = np.zeros(M + 2)
    C_r = np.zeros(M + 2)
    D_l = np.zeros(M + 2)
    D_r = np.zeros(M + 2)

    # Заполняем коэффициенты
    for i in range(2, M + 1):
        A_val = 0.3 * math.sin(i) / V
        A_l[i] = A_val - Rad
        A_r[i] = A_val + Rad

    for i in range(1, M + 1):
        B_val = 10 * V + i / V
        B_l[i] = B_val - Rad
        B_r[i] = B_val + Rad

    for i in range(1, M):
        C_val = 0.4 * math.cos(i) / V
        C_l[i] = C_val - Rad
        C_r[i] = C_val + Rad

    for i in range(1, M + 1):
        D_val = 1.3 + i / V
        D_l[i] = D_val - Rad
        D_r[i] = D_val + Rad

    # Вывод коэффициентов для M=8
    if M == 8:
        print("\nКОЭФФИЦИЕНТЫ СИСТЕМЫ:")
        print("i\tA_i\t\t\tB_i\t\t\tC_i\t\t\tD_i")
        print("-" * 100)
        for i in range(1, M + 1):
            A_str = f"[{A_l[i]:.6e}, {A_r[i]:.6e}]" if i >= 2 else "0.0"
            B_str = f"[{B_l[i]:.6e}, {B_r[i]:.6e}]"
            C_str = f"[{C_l[i]:.6e}, {C_r[i]:.6e}]" if i < M else "0.0"
            D_str = f"[{D_l[i]:.6e}, {D_r[i]:.6e}]"
            print(f"{i}\t{A_str}\t{B_str}\t{C_str}\t{D_str}")

    # Для нахождения ЛЕВОЙ границы решения (минимальные x_i)
    alpha_min = np.zeros(M + 2)
    beta_min = np.zeros(M + 2)
    x_min = np.zeros(M + 2)

    # Прямой ход для минимизации
    alpha_min[1] = -C_r[1] / B_r[1]  # берем правые границы чтобы уменьшить |alpha|
    beta_min[1] = D_l[1] / B_r[1]  # берем левую D и правый B

    for i in range(2, M):
        denom = B_r[i] + A_r[i] * alpha_min[i - 1]
        alpha_min[i] = -C_r[i] / denom
        beta_min[i] = (D_l[i] - A_l[i] * beta_min[i - 1]) / denom

    # Для последнего уравнения
    x_min[M] = (D_l[M] - A_l[M] * beta_min[M - 1]) / (B_r[M] + A_r[M] * alpha_min[M - 1])

    # Обратный ход
    for i in range(M - 1, 0, -1):
        x_min[i] = alpha_min[i] * x_min[i + 1] + beta_min[i]

    # Для нахождения ПРАВОЙ границы решения (максимальные x_i)
    alpha_max = np.zeros(M + 2)
    beta_max = np.zeros(M + 2)
    x_max = np.zeros(M + 2)

    # Прямой ход для максимизации
    alpha_max[1] = -C_l[1] / B_l[1]  # берем левые границы чтобы увеличить |alpha|
    beta_max[1] = D_r[1] / B_l[1]  # берем правую D и левый B

    for i in range(2, M):
        denom = B_l[i] + A_l[i] * alpha_max[i - 1]
        alpha_max[i] = -C_l[i] / denom
        beta_max[i] = (D_r[i] - A_r[i] * beta_max[i - 1]) / denom

    # Для последнего уравнения
    x_max[M] = (D_r[M] - A_r[M] * beta_max[M - 1]) / (B_l[M] + A_l[M] * alpha_max[M - 1])

    # Обратный ход
    for i in range(M - 1, 0, -1):
        x_max[i] = alpha_max[i] * x_max[i + 1] + beta_max[i]

    # Формируем интервальное решение
    x_interval = []
    for i in range(1, M + 1):
        x_l = min(x_min[i], x_max[i])
        x_r = max(x_min[i], x_max[i])
        x_interval.append((x_l, x_r))

    # Вычисляем невязку
    residual_interval = []
    for i in range(1, M + 1):
        if i == 1:
            # B₁·x₁ + C₁·x₂ = D₁
            res_min = B_l[i] * x_min[i] + C_l[i] * x_min[i + 1] - D_r[i]
            res_max = B_r[i] * x_max[i] + C_r[i] * x_max[i + 1] - D_l[i]
        elif i == M:
            # A_M·x_{M-1} + B_M·x_M = D_M
            res_min = A_l[i] * x_min[i - 1] + B_l[i] * x_min[i] - D_r[i]
            res_max = A_r[i] * x_max[i - 1] + B_r[i] * x_max[i] - D_l[i]
        else:
            # A_i·x_{i-1} + B_i·x_i + C_i·x_{i+1} = D_i
            res_min = (A_l[i] * x_min[i - 1] + B_l[i] * x_min[i] +
                       C_l[i] * x_min[i + 1] - D_r[i])
            res_max = (A_r[i] * x_max[i - 1] + B_r[i] * x_max[i] +
                       C_r[i] * x_max[i + 1] - D_l[i])

        res_l = min(res_min, res_max)
        res_r = max(res_min, res_max)
        residual_interval.append((res_l, res_r))

    return x_interval, residual_interval


# Основная программа
V = 11

print("=" * 80)
print("ИСЛАУ с 3-диагональной матрицей методом прогонки")
print(f"Вариант: V = {V}")
print("=" * 80)

# Решение для M = 8 (полный вывод)
print("\n1. РЕШЕНИЕ ДЛЯ M = 8:")
print("-" * 80)

M1 = 8
x_sol1, residual1 = solve_tridiagonal_interval(V, M1)

print("\nИНТЕРВАЛЬНОЕ РЕШЕНИЕ (формат: [min, max]):")
for i, (x_l, x_r) in enumerate(x_sol1, 1):
    print(f"x[{i}] = [{x_l:.6e}, {x_r:.6e}]")

print("\nИНТЕРВАЛЬНАЯ НЕВЯЗКА (формат: [min, max]):")
for i, (res_l, res_r) in enumerate(residual1, 1):
    print(f"r[{i}] = [{res_l:.3e}, {res_r:.3e}]")

# Решение для M = 1000000 (вывод 4 значений)
print("\n" + "=" * 80)
print("2. РЕШЕНИЕ ДЛЯ M = 1000000 (значения с 500001 по 500004):")
print("-" * 80)

M2 = 1000000
x_sol2, residual2 = solve_tridiagonal_interval(V, M2)

print("\nИнтервальное решение:")
for i in range(500000, 500004):
    x_l, x_r = x_sol2[i]
    print(f"x[{i + 1}] = [{x_l:.6e}, {x_r:.6e}]")

print("\nИнтервальная невязка:")
for i in range(500000, 500004):
    res_l, res_r = residual2[i]
    print(f"r[{i + 1}] = [{res_l:.3e}, {res_r:.3e}]")

print("\n" + "=" * 80)
