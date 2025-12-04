import math
from typing import List
import sys


class Interval:
    def __init__(self, lower: float = 0, upper: float = 0):
        self.lower = lower
        self.upper = upper

    @property
    def width(self) -> float:
        return self.upper - self.lower

    @property
    def mid(self) -> float:
        return (self.lower + self.upper) / 2.0

    def __add__(self, other: 'Interval') -> 'Interval':
        return Interval(self.lower + other.lower, self.upper + other.upper)

    def __sub__(self, other: 'Interval') -> 'Interval':
        return Interval(self.lower - other.upper, self.upper - other.lower)

    def __mul__(self, other: 'Interval') -> 'Interval':
        if isinstance(other, (int, float)):
            other = Interval(other, other)
        vals = [
            self.lower * other.lower,
            self.lower * other.upper,
            self.upper * other.lower,
            self.upper * other.upper
        ]
        return Interval(min(vals), max(vals))

    def __rmul__(self, scalar: float) -> 'Interval':
        return self * Interval(scalar, scalar)

    def __truediv__(self, other: 'Interval') -> 'Interval':
        if other.lower <= 0 and other.upper >= 0:
            print("Деление на интервал, содержащий 0!", file=sys.stderr)
            return Interval(-1e10, 1e10)

        vals = [
            self.lower / other.lower,
            self.lower / other.upper,
            self.upper / other.lower,
            self.upper / other.upper
        ]
        return Interval(min(vals), max(vals))

    def __str__(self, precision: int = 6) -> str:
        return f"[{self.lower:.{precision}f}, {self.upper:.{precision}f}]"

    def __repr__(self) -> str:
        return f"Interval({self.lower}, {self.upper})"


def dot_product(a: List[Interval], b: List[Interval]) -> Interval:
    """Скалярное произведение интервальных векторов"""
    result = Interval(0, 0)
    for ai, bi in zip(a, b):
        result = result + (ai * bi)
    return result


def norm(v: List[Interval]) -> Interval:
    """Норма интервального вектора"""
    sum_sq = Interval(0, 0)
    for x in v:
        sum_sq = sum_sq + (x * x)
    return Interval(math.sqrt(sum_sq.lower), math.sqrt(sum_sq.upper))


def print_matrix(A: List[List[Interval]], file=None, precision: int = 4):
    """Вывод интервальной матрицы"""
    for row in A:
        for elem in row:
            if file:
                file.write(f"{elem:20}")
            else:
                print(f"{elem:20}", end="")
        if file:
            file.write("\n")
        else:
            print()


def print_vector(v: List[Interval], file=None, precision: int = 6):
    """Вывод интервального вектора"""
    for elem in v:
        if file:
            file.write(f"{elem:22}")
        else:
            print(f"{elem:22}", end="")
    if file:
        file.write("\n")
    else:
        print()


def householder_qr(A: List[List[Interval]], b: List[Interval], N: int) -> None:
    """Метод отражений Хаусхолдера для интервальных матриц"""
    for k in range(N - 1):
        # Формируем вектор x для текущего столбца
        x = [A[i][k] for i in range(k, N)]

        # Вычисляем норму x
        x_norm = norm(x)

        # Формируем вектор v
        v = x.copy()
        v[0] = v[0] + (x_norm if x[0].lower >= 0 else Interval(-1, -1) * x_norm)

        # Норма вектора v
        v_norm = norm(v)

        # Если норма v близка к нулю, пропускаем шаг
        if v_norm.lower < 1e-12:
            continue

        # Нормализуем v
        for i in range(len(v)):
            v[i] = v[i] / v_norm

        # Применяем отражение к подматрице A
        for j in range(k, N):
            col = [A[i][j] for i in range(k, N)]
            dot = dot_product(v, col) * Interval(2, 2)

            for i in range(k, N):
                A[i][j] = A[i][j] - (v[i - k] * dot)

        # Применяем отражение к вектору b
        b_sub = [b[i] for i in range(k, N)]
        dot_b = dot_product(v, b_sub) * Interval(2, 2)

        for i in range(k, N):
            b[i] = b[i] - (v[i - k] * dot_b)


def back_substitution(U: List[List[Interval]], b: List[Interval]) -> List[Interval]:
    """Обратный ход для интервальной треугольной системы"""
    N = len(b)
    x = [Interval(0, 0) for _ in range(N)]

    for i in range(N - 1, -1, -1):
        sum_int = Interval(0, 0)
        for j in range(i + 1, N):
            sum_int = sum_int + (U[i][j] * x[j])
        x[i] = (b[i] - sum_int) / U[i][i]

    return x


def compute_residual(A: List[List[Interval]], b: List[Interval], x: List[Interval]) -> List[Interval]:
    """Вычисление невязки"""
    N = len(A)
    residual = [Interval(0, 0) for _ in range(N)]

    for i in range(N):
        sum_int = Interval(0, 0)
        for j in range(N):
            sum_int = sum_int + (A[i][j] * x[j])
        residual[i] = b[i] - sum_int

    return residual


def compute_width(x: List[Interval]) -> List[float]:
    """Вычисление ширины вектора"""
    return [elem.width for elem in x]


def main():
    N = 6
    V = 11
    Rad = 0.0001

    try:
        with open("result_python.txt", "w", encoding="utf-8") as out_file:
            # Инициализация матрицы A и вектора b
            A = [[Interval(0, 0) for _ in range(N)] for _ in range(N)]
            b = [Interval(0, 0) for _ in range(N)]

            out_file.write("Интервальная матрица A:\n")
            for i in range(N):
                for j in range(N):
                    if i == j:
                        mid = abs(99 + math.sin(i + 1) / V)
                        A[i][j] = Interval(mid - Rad, mid + Rad)
                    else:
                        mid = -abs(0.01 * V + math.sin(i - j))
                        A[i][j] = Interval(mid - Rad, mid + Rad)

            # Форматированный вывод матрицы A
            for row in A:
                for elem in row:
                    out_file.write(f"[{elem.lower:8.4f}, {elem.upper:8.4f}] ")
                out_file.write("\n")
            out_file.write("\n")

            out_file.write("Интервальный вектор b:\n")
            for j in range(N):
                mid = 2 * math.cos(j + 1 + V)
                b[j] = Interval(mid - Rad, mid + Rad)

            # Форматированный вывод вектора b
            for elem in b:
                out_file.write(f"[{elem.lower:8.4f}, {elem.upper:8.4f}] ")
            out_file.write("\n\n")

            # Сохраняем копии исходных данных
            A_orig = [[Interval(A[i][j].lower, A[i][j].upper) for j in range(N)] for i in range(N)]
            b_orig = [Interval(b[i].lower, b[i].upper) for i in range(N)]

            # QR разложение методом Хаусхолдера
            householder_qr(A, b, N)

            out_file.write("Интервальная треугольная матрица:\n")
            for row in A:
                for elem in row:
                    out_file.write(f"[{elem.lower:8.4f}, {elem.upper:8.4f}] ")
                out_file.write("\n")
            out_file.write("\n")

            out_file.write("Преобразованный вектор b:\n")
            for elem in b:
                out_file.write(f"[{elem.lower:8.4f}, {elem.upper:8.4f}]\n")
            out_file.write("\n")

            # Решение системы
            x = back_substitution(A, b)

            out_file.write("Интервальный вектор X:\n")
            for elem in x:
                out_file.write(f"[{elem.lower:10.6f}, {elem.upper:10.6f}] ")
            out_file.write("\n\n")

            # Ширина вектора X
            widths = compute_width(x)
            out_file.write("Ширина вектора wid(X):\n")
            for w in widths:
                out_file.write(f"{w:10.6f}")
            out_file.write("\n\n")

            # Вектор невязки
            residual = compute_residual(A_orig, b_orig, x)
            out_file.write("Вектор невязки:\n")
            for elem in residual:
                out_file.write(f"[{elem.lower:10.6f}, {elem.upper:10.6f}]\n")

            print("Результаты записаны в файл result_python.txt")

    except IOError as e:
        print(f"Не удалось открыть файл для записи: {e}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
