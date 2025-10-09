from math import sin

from common import Interval


def main():
    N = int(input('Введите N: '))
    V = 11
    R = 0.001

    intervals = [Interval(sin(V + i) - R, sin(V + i) + R) for i in range(1, N + 1)]
    print(f'Массив: {intervals}')
    print(f'Сумма интервалов: {sum(intervals)}')

    sorted_intervals = sorted(intervals)
    print(f'Упорядоченный массив: {sorted_intervals}')
    print(f'Сумма упорядоченного массива: {sum(sorted_intervals)}')


if __name__ == '__main__':
    main()
