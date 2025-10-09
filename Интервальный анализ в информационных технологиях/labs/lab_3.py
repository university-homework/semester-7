from math import pi, floor, tan, inf

from common import Interval


def main():
    a = float(input('Начало интервала a: '))
    b = float(input('Конец интервала b: '))
    N = int(input('Количество точек N: '))
    R = float(input('Радиус интервалов R: '))
    h = (b - a) / (N - 1)
    build_interval_table(a, b, h, N, R)


def build_interval_table(a, b, h, N, R):
    for i in range(N):
        x_center = a + i * h

        left_point = x_center - R
        right_point = x_center + R

        Xi = Interval(left_point, right_point)
        f_Xi = f(Xi)

        print(f"{x_center} {Xi} {f_Xi}")


def f(X):
    return 7 + 8 * X - tan_interval(X + 1)


def tan_interval(interval):
    asymptotes = []
    k = floor((interval.start - pi / 2) / pi) + 1

    while True:
        asymptote = pi / 2 + pi * k
        if interval.start <= asymptote <= interval.end:
            asymptotes.append(asymptote)
            k += 1
        else:
            break

    if not asymptotes:
        tan_start = tan(interval.start)
        tan_end = tan(interval.end)
        return Interval(min(tan_start, tan_end), max(tan_start, tan_end))

    return Interval(-inf, inf)


if __name__ == '__main__':
    main()
