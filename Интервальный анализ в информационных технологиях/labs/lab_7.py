import math


class Interval:
    def __init__(self, start, end):
        self.start = float(start)
        self.end = float(end)

    # ---------- СТАНДАРТНЫЕ операции ----------
    def __add__(self, other):
        if isinstance(other, Interval):
            return Interval(self.start + other.start, self.end + other.end)
        if isinstance(other, (int, float)):
            return Interval(self.start + other, self.end + other)
        return NotImplemented

    def __radd__(self, other):
        return self.__add__(other)

    def __mul__(self, other):
        if isinstance(other, Interval):
            products = (
                self.start * other.start,
                self.start * other.end,
                self.end * other.start,
                self.end * other.end,
            )
            return Interval(min(products), max(products))
        if isinstance(other, (int, float)):
            return Interval(self.start * other, self.end * other)
        return NotImplemented

    def __rmul__(self, other):
        return self.__mul__(other)

    # ---------- НЕСТАНДАРТНЫЕ операции ----------
    def __sub__(self, other):
        """Нестандартное вычитание: [a,b] - [c,d] = [a - c, b - d]"""
        if isinstance(other, Interval):
            subs = [
                self.start - other.start,
                self.end - other.end,
            ]
            return Interval(min(subs), max(subs))
        if isinstance(other, (int, float)):
            return Interval(self.start - other, self.end - other)
        return NotImplemented

    def __truediv__(self, other):
        if isinstance(other, Interval):
            if self.start > 0 and other.start > 0:
                divs = [
                    self.start / other.start,
                    self.end / other.end,
                ]
                return Interval(min(divs), max(divs))
            elif self.end < 0 and other.end < 0:
                divs = [
                    self.start / other.start,
                    self.end / other.end,
                ]
                return Interval(min(divs), max(divs))
            elif self.start > 0 > other.end:
                divs = [
                    self.start / other.end,
                    self.end / other.start,
                ]
                return Interval(min(divs), max(divs))
            elif self.end < 0 < other.start:
                divs = [
                    self.start / other.end,
                    self.end / other.start,
                ]
                return Interval(min(divs), max(divs))
            elif self.start <= 0 <= self.end and other.start > 0:
                divs = [
                    self.start / other.end,
                    self.end / other.end,
                ]
                return Interval(min(divs), max(divs))
            elif self.start <= 0 <= self.end and other.end < 0:
                divs = [
                    self.start / other.start,
                    self.end / other.start,
                ]
                return Interval(min(divs), max(divs))
            elif self.start > 0 and other.start <= 0 <= other.end and abs(self.end) - abs(self.start) > abs(other.end) - abs(other.start):
                divs = [
                    self.start / other.start,
                    self.end / other.end,
                ]
                return Interval(min(divs), max(divs))
            elif self.start > 0 and other.start <= 0 <= other.end and abs(self.end) - abs(self.start) <= abs(other.end) - abs(other.start):
                divs = [
                    self.start / other.start,
                    self.start / other.end,
                ]
                return Interval(min(divs), max(divs))
            elif self.end < 0 and other.start <= 0 <= other.end and abs(self.end) - abs(self.start) > abs(other.end) - abs(other.start):
                divs = [
                    self.start / other.start,
                    self.end / other.end,
                ]
                return Interval(min(divs), max(divs))
            elif self.end < 0 and other.start <= 0 <= other.end and abs(self.end) - abs(self.start) <= abs(other.end) - abs(other.start):
                divs = [
                    self.end / other.start,
                    self.end / other.end,
                ]
                return Interval(min(divs), max(divs))
            elif self.start <= 0 <= self.end and other.start <= 0 <= other.end and abs(self.end) - abs(self.start) >= abs(other.end) - abs(other.start):
                divs = [
                    self.end / other.start,
                    self.end / other.end,
                ]
                return Interval(min(divs), max(divs))
            elif self.start <= 0 <= self.end and other.start <= 0 <= other.end and abs(self.end) - abs(self.start) < abs(other.end) - abs(other.start):
                divs = [
                    self.end / other.start,
                    self.start / other.start,
                ]
                return Interval(min(divs), max(divs))
            raise ValueError

        elif isinstance(other, (int, float)):
            return Interval(self.start / other, self.end / other)
        raise NotImplemented

    def __repr__(self):
        return f"Interval({self.start:.6e}, {self.end:.6e})"

    def __str__(self):
        return f"[{self.start:.6e}, {self.end:.6e}]"


# ---------- Метод прогонки с нестандартными операциями ----------
def solve_tridiagonal_interval(V, M):
    Rad = 0.01

    # Интервальные коэффициенты
    A, B, C, D = [None]*M, [None]*M, [None]*M, [None]*M

    for i in range(1, M):
        a_val = 0.3 * math.sin(i + 1) / V
        A[i] = Interval(a_val - Rad, a_val + Rad)
    A[0] = Interval(0, 0)

    for i in range(M):
        b_val = 10 * V + (i + 1) / V
        B[i] = Interval(b_val - Rad, b_val + Rad)

    for i in range(M - 1):
        c_val = 0.4 * math.cos(i + 1) / V
        C[i] = Interval(c_val - Rad, c_val + Rad)
    C[M - 1] = Interval(0, 0)

    for i in range(M):
        d_val = 1.3 + (i + 1) / V
        D[i] = Interval(d_val - Rad, d_val + Rad)

    # Векторы альфа, бета, x
    alpha = [None]*M
    beta = [None]*M
    x = [None]*M

    neg_one = Interval(-1, -1)

    # ---------- Прямой ход с Interval ----------
    alpha[0] = (neg_one * C[0]) / B[0]
    beta[0] = D[0] / B[0]

    for i in range(1, M - 1):
        denom = B[i] + (A[i] * alpha[i - 1])
        alpha[i] = (neg_one * C[i]) / denom
        beta[i] = (D[i] - (A[i] * beta[i - 1])) / denom

    # Последний элемент
    denom_last = B[M - 1] + (A[M - 1] * alpha[M - 2])
    x[M - 1] = (D[M - 1] - (A[M - 1] * beta[M - 2])) / denom_last

    # ---------- Обратный ход с Interval ----------
    for i in range(M - 2, -1, -1):
        x[i] = (alpha[i] * x[i + 1]) + beta[i]

    return x, A, B, C, D



# ---------- Невязка ----------
def calculate_residual_nonstandard(A, B, C, D, x):
    n = len(B)
    residual = []

    for i in range(n):
        if i == 0:
            res_i = B[i] * x[i] + C[i] * x[i + 1] - D[i]
        elif i == n - 1:
            res_i = A[i] * x[i - 1] + B[i] * x[i] - D[i]
        else:
            res_i = A[i] * x[i - 1] + B[i] * x[i] + C[i] * x[i + 1] - D[i]

        # res_i уже Interval, просто берем его границы
        residual.append((res_i.start, res_i.end))

    return residual


# ---------- Основная программа ----------
if __name__ == "__main__":
    V = 11
    M = 8

    print("=" * 80)
    print("ИСЛАУ с 3-диагональной матрицей методом прогонки (НЕСТАНДАРТНЫЕ операции)")
    print(f"Вариант: V = {V}, M = {M}")
    print("=" * 80)

    x_sol, A, B, C, D = solve_tridiagonal_interval(V, M)
    residual = calculate_residual_nonstandard(A, B, C, D, x_sol)

    print("\nИНТЕРВАЛЬНОЕ РЕШЕНИЕ:")
    for i, xi in enumerate(x_sol, 1):
        print(f"x[{i}] = {xi}")

    print("\nИНТЕРВАЛЬНАЯ НЕВЯЗКА:")
    for i, ri in enumerate(residual, 1):
        print(f"r[{i}] = [{ri[0]:.10e}, {ri[1]:.10e}]")

    print("\n" + "=" * 80)

    x_sol2, A2, B2, C2, D2 = solve_tridiagonal_interval(V, 1_000_000)
    residual2 = calculate_residual_nonstandard(A2, B2, C2, D2, x_sol2)

    print("\nИНТЕРВАЛЬНОЕ РЕШЕНИЕ:")
    for i in range(500000, 500004):
        x_l, x_r = x_sol2[i].start, x_sol2[i].end
        print(f"x[{i + 1}] = [{x_l:.6e}, {x_r:.6e}]")

    print("\nИНТЕРВАЛЬНАЯ НЕВЯЗКА:")
    for i in range(500000, 500004):
        res_l, res_r = residual2[i][0], residual2[i][1]
        print(f"r[{i + 1}] = [{res_l:.10e}, {res_r:.10e}]")

    print("\n" + "=" * 80)
