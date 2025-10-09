from common import Interval


def main():
    X = Interval(float(input('Начало: ')), float(input('Конец: ')))
    print(f(X))


def f(X):
    return -3 + 3 * X - 6 * X ** 2 + 2 * X ** 3


if __name__ == '__main__':
    main()
