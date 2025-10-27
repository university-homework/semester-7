import numpy as np
import math

V = 11
r = 0.005


def a_ij(i, j):
    if i == j:
        return 31 + V * math.sin(i)
    else:
        return 0.01 * V + math.log(i + j)


def b_j(j):
    return (2.7 * V) / math.log(6 + j)


# Создаем матрицу A и вектор b (середины)
A_mid = np.zeros((4, 4))
b_mid = np.zeros(4)

for i in range(4):
    for j in range(4):
        A_mid[i, j] = a_ij(i + 1, j + 1)
    b_mid[i] = b_j(i + 1)

# Создаем интервальные матрицу и вектор
A_interval = np.zeros((4, 4, 2))
b_interval = np.zeros((4, 2))

for i in range(4):
    for j in range(4):
        A_interval[i, j, 0] = A_mid[i, j] - r
        A_interval[i, j, 1] = A_mid[i, j] + r
    b_interval[i, 0] = b_mid[i] - r
    b_interval[i, 1] = b_mid[i] + r

# Умножение A * b в интервальной арифметике
C_interval = np.zeros((4, 2))

for i in range(4):
    lower_sum = 0
    upper_sum = 0
    for j in range(4):
        # Умножение интервалов [a1,a2] * [b1,b2]
        a_low = A_interval[i, j, 0]
        a_high = A_interval[i, j, 1]
        b_low = b_interval[j, 0]
        b_high = b_interval[j, 1]

        # Все комбинации произведений
        products = [a_low * b_low, a_low * b_high, a_high * b_low, a_high * b_high]
        lower_sum += min(products)
        upper_sum += max(products)

    C_interval[i, 0] = lower_sum
    C_interval[i, 1] = upper_sum

# Преобразование в форму "середина-радиус"
C_mid_rad = np.zeros((4, 2))
for i in range(4):
    C_mid_rad[i, 0] = (C_interval[i, 0] + C_interval[i, 1]) / 2  # середина
    C_mid_rad[i, 1] = (C_interval[i, 1] - C_interval[i, 0]) / 2  # радиус

# Вывод результатов
print("Интервальная матрица A:")
for i in range(4):
    for j in range(4):
        print(f"[{A_interval[i, j, 0]:.3f}, {A_interval[i, j, 1]:.3f}]", end=" ")
    print()

print("\nИнтервальный вектор b:")
for i in range(4):
    print(f"[{b_interval[i, 0]:.3f}, {b_interval[i, 1]:.3f}]")

print("\nИнтервальный вектор C = A * b (середина-радиус):")
for i in range(4):
    print(f"({C_mid_rad[i, 0]:.3f} ± {C_mid_rad[i, 1]:.3f})")
