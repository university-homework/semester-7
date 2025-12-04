import math
from typing import List, Tuple


class Interval:
    def __init__(self, l: float, r: float):
        self.l = l
        self.r = r

    def __str__(self, precision=4, width=7):
        fmt = f"[{{:{width}.{precision}f}},{{:{width}.{precision}f}}]"
        return fmt.format(self.l, self.r)

    def width(self) -> float:
        return self.r - self.l


def interval_str_4(iv: Interval) -> str:
    return f"[{iv.l:7.4f},{iv.r:7.4f}]"


def interval_str_6(iv: Interval) -> str:
    return f"[{iv.l:10.6f},{iv.r:10.6f}]"


def add(a: Interval, b: Interval) -> Interval:
    return Interval(a.l + b.l, a.r + b.r)


def sub(a: Interval, b: Interval) -> Interval:
    return Interval(a.l - b.r, a.r - b.l)


def mul(a: Interval, b: Interval) -> Interval:
    products = [a.l * b.l, a.l * b.r, a.r * b.l, a.r * b.r]
    return Interval(min(products), max(products))


def divi(a: Interval, b: Interval) -> Interval:
    if b.l <= 0 and b.r >= 0:
        raise ValueError("Деление на интервал, содержащий ноль!")
    quotients = [a.l / b.l, a.l / b.r, a.r / b.l, a.r / b.r]
    return Interval(min(quotients), max(quotients))


def mulc(c: float, a: Interval) -> Interval:
    if c >= 0:
        return Interval(c * a.l, c * a.r)
    else:
        return Interval(c * a.r, c * a.l)


def hypot_interval(a: Interval, b: Interval) -> Interval:
    values = [
        math.hypot(a.l, b.l),
        math.hypot(a.l, b.r),
        math.hypot(a.r, b.l),
        math.hypot(a.r, b.r)
    ]
    return Interval(min(values), max(values))


def givens_qr_solve(A: List[List[Interval]], b: List[Interval]) -> Tuple[
    List[List[Interval]], List[Interval], List[Interval]]:
    N = len(A)
    R = [row[:] for row in A]  # Копируем матрицу A
    y = b[:]  # Копируем вектор b

    # Полностью интервальные вращения Гивенса
    for j in range(N):
        for i in range(j + 1, N):
            r = hypot_interval(R[j][j], R[i][j])
            if r.l < 1e-12:
                continue

            c = divi(R[j][j], r)  # c = R[j][j]/r
            s = mulc(-1.0, divi(R[i][j], r))  # s = -R[i][j]/r

            for k in range(N):
                t1 = sub(mul(c, R[j][k]), mul(s, R[i][k]))
                t2 = add(mul(s, R[j][k]), mul(c, R[i][k]))
                R[j][k] = t1
                R[i][k] = t2

            t1y = sub(mul(c, y[j]), mul(s, y[i]))
            t2y = add(mul(s, y[j]), mul(c, y[i]))
            y[j] = t1y
            y[i] = t2y

    # Обратная подстановка
    X = [Interval(0, 0) for _ in range(N)]
    for i in range(N - 1, -1, -1):
        s = Interval(0, 0)
        for j in range(i + 1, N):
            s = add(s, mul(R[i][j], X[j]))
        num = sub(y[i], s)
        X[i] = divi(num, R[i][i])

    # Вычисление невязки
    res = [Interval(0, 0) for _ in range(N)]
    for i in range(N):
        s = Interval(0, 0)
        for j in range(N):
            s = add(s, mul(A[i][j], X[j]))
        res[i] = sub(s, b[i])

    return R, y, X, res


def main():
    N = 5
    V = 11
    rad = 0.0001

    # Инициализация интервальной матрицы A и вектора b
    A = [[Interval(0, 0) for _ in range(N)] for _ in range(N)]
    b = [Interval(0, 0) for _ in range(N)]

    for i in range(N):
        for j in range(N):
            if i == j:
                val = abs(77 + math.sin(i + 1) / V)
            else:
                val = -abs(0.01 * V + math.sin(i - j))
            A[i][j] = Interval(val - rad, val + rad)

        valb = 2 * math.cos(i + 1 + V)
        b[i] = Interval(valb - rad, valb + rad)

    # Решение системы
    R, y, X, res = givens_qr_solve(A, b)

    # Вывод результатов
    with open("interval_output_python.txt", "w", encoding="utf-8") as fout:
        def output(s):
            print(s, end="")
            fout.write(s)

        output("Интервальная матрица A (формат 7:4):\n")
        for i in range(N):
            for j in range(N):
                output(interval_str_4(A[i][j]) + " ")
            output("\n")

        output("\nИнтервальный вектор b (формат 7:4):\n")
        for i in range(N):
            output(interval_str_4(b[i]) + " ")
        output("\n\n")

        output("Верхнетреугольная матрица R (формат 7:4):\n")
        for i in range(N):
            for j in range(N):
                output(interval_str_4(R[i][j]) + " ")
            output("\n")

        output("\nМодифицированный вектор b после преобразования Гивенса (формат 7:4):\n")
        for i in range(N):
            output(interval_str_4(y[i]) + "\n")

        output("\nИнтервальный вектор X (формат 10:6):\n")
        for i in range(N):
            output(interval_str_6(X[i]) + " ")
        output("\n")

        output("\nШирина вектора wid(X) (формат 10:6):\n")
        for i in range(N):
            width_val = X[i].width()
            output(f"{width_val:10.6f} ")
        output("\n")

        output("\nВектор невязки (формат 10:6):\n")
        for i in range(N):
            output(interval_str_6(res[i]) + "\n")

        output("\nГотово. Результаты сохранены в interval_output_python.txt\n")


if __name__ == "__main__":
    main()
