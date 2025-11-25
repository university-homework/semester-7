import math


# Класс интервала
class Interval:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    # Сумма интервалов
    def __add__(self, other):
        return Interval(self.left + other.left, self.right + other.right)

    # Разность интервалов
    def __sub__(self, other):
        return Interval(self.left - other.right, self.right - other.left)

    # Умножение интервалов
    def __mul__(self, other):
        p1 = self.left * other.left
        p2 = self.left * other.right
        p3 = self.right * other.left
        p4 = self.right * other.right
        return Interval(min(p1, p2, p3, p4), max(p1, p2, p3, p4))

    # Деление интервалов
    def __truediv__(self, other):
        p1 = self.left / other.left
        p2 = self.left / other.right
        p3 = self.right / other.left
        p4 = self.right / other.right
        return Interval(min(p1, p2, p3, p4), max(p1, p2, p3, p4))

# Параметры
N = 5
V = 11.0
rad = 0.01

# Формирование матрицы и вектора
A = [[None]*N for _ in range(N)]
b = [None]*N

for i in range(N):
    for j in range(N):
        if i == j:
            val = 31 + math.sin(i + 1) / V
        else:
            val = 0.01 * V + math.sin((i + 1) - (j + 1))
        A[i][j] = Interval(val - rad, val + rad)
    bv = 10 * math.cos((i + 1) + V)
    b[i] = Interval(bv - rad, bv + rad)

# Метод Гаусса
Ab = [row[:] + [b[i]] for i, row in enumerate(A)]

# Прямой ход
for k in range(N):
    pivot = Ab[k][k]
    for j in range(k, N + 1):
        Ab[k][j] = Ab[k][j] / pivot
    for i in range(k + 1, N):
        factor = Ab[i][k]
        for j in range(k, N + 1):
            Ab[i][j] = Ab[i][j] - factor * Ab[k][j]

# Обратный ход
x = [Interval(0, 0) for _ in range(N)]
for i in range(N - 1, -1, -1):
    sum_ = Interval(0, 0)
    for j in range(i + 1, N):
        sum_ = sum_ + Ab[i][j] * x[j]
    x[i] = Ab[i][N] - sum_

# Вектор невязки
r = [Interval(0, 0) for _ in range(N)]
for i in range(N):
    sum_ = Interval(0, 0)
    for j in range(N):
        sum_ = sum_ + A[i][j] * x[j]
    r[i] = sum_ - b[i]

# Сохраняем результаты в файл
with open("result.txt", "w") as f:
    # Интервальная матрица A и вектор b (:7:3)
    f.write("Интервальная матрица A и вектор b:\n")
    for i in range(N):
        f.write(" ".join(f"[{A[i][j].left:7.3f},{A[i][j].right:7.3f}]" for j in range(N)))
        f.write(" | " + f"[{b[i].left:7.3f},{b[i].right:7.3f}]\n")

    # Интервальная треугольная матрица (:7:3)
    f.write("\nИнтервальная треугольная матрица и вектор:\n")
    for i in range(N):
        f.write(" ".join(f"[{Ab[i][j].left:7.3f},{Ab[i][j].right:7.3f}]" for j in range(N)))
        f.write(" | " + f"[{Ab[i][N].left:7.3f},{Ab[i][N].right:7.3f}]\n")

    # Интервальный вектор X и вектор невязки (:10:6)
    f.write("\nИнтервальный вектор X и вектор невязки:\n")
    for i in range(N):
        f.write(f"[{x[i].left:10.6f},{x[i].right:10.6f}] | [{r[i].left:10.6f},{r[i].right:10.6f}]\n")

print("Результаты сохранены в файл result.txt")
