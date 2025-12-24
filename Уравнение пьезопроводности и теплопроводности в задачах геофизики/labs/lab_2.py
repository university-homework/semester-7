import numpy as np
import matplotlib.pyplot as plt


# Функции для системы дифференциальных уравнений
def f1(t, x, y, z):
    return y  # dx/dt = y


def f2(t, x, y, z):
    return z  # dy/dt = z


def f3(t, x, y, z):
    return 11  # dz/dt = 11


# Точное решение
def exact_solution(t):
    x_exact = ((11 * t ** 3) / 6) + (t ** 2) / 2 + t + 1
    y_exact = (11 * t ** 2) / 2 + t + 1
    z_exact = 11 * t + 1
    return x_exact, y_exact, z_exact


# Метод Рунге-Кутта 4-го порядка для системы трех уравнений
def runge_kutta_system(t_span, x0, y0, z0, h):
    t0, t_n = t_span
    n = int((t_n - t0) / h) + 1
    t = np.linspace(t0, t_n, n)

    x = np.zeros(n)
    y = np.zeros(n)
    z = np.zeros(n)

    x[0] = x0
    y[0] = y0
    z[0] = z0

    for i in range(n - 1):
        # Коэффициенты для x
        k1_x = f1(t[i], x[i], y[i], z[i])
        k1_y = f2(t[i], x[i], y[i], z[i])
        k1_z = f3(t[i], x[i], y[i], z[i])

        k2_x = f1(t[i] + h / 2, x[i] + (h / 2) * k1_x, y[i] + (h / 2) * k1_y, z[i] + (h / 2) * k1_z)
        k2_y = f2(t[i] + h / 2, x[i] + (h / 2) * k1_x, y[i] + (h / 2) * k1_y, z[i] + (h / 2) * k1_z)
        k2_z = f3(t[i] + h / 2, x[i] + (h / 2) * k1_x, y[i] + (h / 2) * k1_y, z[i] + (h / 2) * k1_z)

        k3_x = f1(t[i] + h / 2, x[i] + (h / 2) * k2_x, y[i] + (h / 2) * k2_y, z[i] + (h / 2) * k2_z)
        k3_y = f2(t[i] + h / 2, x[i] + (h / 2) * k2_x, y[i] + (h / 2) * k2_y, z[i] + (h / 2) * k2_z)
        k3_z = f3(t[i] + h / 2, x[i] + (h / 2) * k2_x, y[i] + (h / 2) * k2_y, z[i] + (h / 2) * k2_z)

        k4_x = f1(t[i] + h, x[i] + h * k3_x, y[i] + h * k3_y, z[i] + h * k3_z)
        k4_y = f2(t[i] + h, x[i] + h * k3_x, y[i] + h * k3_y, z[i] + h * k3_z)
        k4_z = f3(t[i] + h, x[i] + h * k3_x, y[i] + h * k3_y, z[i] + h * k3_z)

        # Обновление значений
        x[i + 1] = x[i] + (h / 6) * (k1_x + 2 * k2_x + 2 * k3_x + k4_x)
        y[i + 1] = y[i] + (h / 6) * (k1_y + 2 * k2_y + 2 * k3_y + k4_y)
        z[i + 1] = z[i] + (h / 6) * (k1_z + 2 * k2_z + 2 * k3_z + k4_z)

    return t, x, y, z


# Параметры решения
t_span = (0, 5)
x0 = 1
y0 = 1
z0 = 1
h = 0.001  # шаг

# Численное решение
t_num, x_rk4, y_rk4, z_rk4 = runge_kutta_system(t_span, x0, y0, z0, h)

# Аналитическое решение для тех же точек времени, что и численное
x_exact_num, y_exact_num, z_exact_num = exact_solution(t_num)

# Аналитическое решение для гладкого графика
t_analytical = np.linspace(0, 5, 1000)
x_exact, y_exact, z_exact = exact_solution(t_analytical)

# Вычисление погрешностей
error_x = np.abs(x_rk4 - x_exact_num)
error_y = np.abs(y_rk4 - y_exact_num)
error_z = np.abs(z_rk4 - z_exact_num)

# Вывод результатов для нескольких точек
print("Численное и аналитическое решение:")
print("t\t\tx_числ\t\tx_аналит\t\ty_числ\t\ty_аналит\t\tz_числ\t\tz_аналит")

for i in range(0, len(t_num), 500):  # выводим каждую 500-ю точку
    print(f"{t_num[i]:.2f}\t\t{x_rk4[i]:.8f}\t{x_exact_num[i]:.8f}\t\t"
          f"{y_rk4[i]:.8f}\t{y_exact_num[i]:.8f}\t\t"
          f"{z_rk4[i]:.8f}\t{z_exact_num[i]:.8f}")

print(f"\nМаксимальные погрешности:")
print(f"Погрешность x(t): {np.max(error_x):.2e}")
print(f"Погрешность y(t): {np.max(error_y):.2e}")
print(f"Погрешность z(t): {np.max(error_z):.2e}")

# Четыре графика на одном листе
plt.figure(figsize=(15, 12))

# График 1: x(t)
plt.subplot(2, 2, 1)
plt.plot(t_num, x_rk4, 'b-', linewidth=2, label='Численное решение')
plt.plot(t_analytical, x_exact, 'r--', linewidth=2, label='Точное решение')
plt.xlabel('Время t')
plt.ylabel('x(t)')
plt.title('Сравнение численного и точного решения для x(t)')
plt.legend()
plt.grid(True)

# График 2: y(t)
plt.subplot(2, 2, 2)
plt.plot(t_num, y_rk4, 'g-', linewidth=2, label='Численное решение')
plt.plot(t_analytical, y_exact, 'm--', linewidth=2, label='Точное решение')
plt.xlabel('Время t')
plt.ylabel('y(t)')
plt.title('Сравнение численного и точного решения для y(t)')
plt.legend()
plt.grid(True)

# График 3: z(t)
plt.subplot(2, 2, 3)
plt.plot(t_num, z_rk4, 'c-', linewidth=2, label='Численное решение')
plt.plot(t_analytical, z_exact, 'y--', linewidth=2, label='Точное решение')
plt.xlabel('Время t')
plt.ylabel('z(t)')
plt.title('Сравнение численного и точного решения для z(t)')
plt.legend()
plt.grid(True)

# График 4: Погрешности
plt.subplot(2, 2, 4)
plt.plot(t_num, error_x, 'b-', linewidth=2, label='Погрешность x(t)')
plt.plot(t_num, error_y, 'g-', linewidth=2, label='Погрешность y(t)')
plt.plot(t_num, error_z, 'r-', linewidth=2, label='Погрешность z(t)')
plt.xlabel('Время t')
plt.ylabel('Абсолютная погрешность')
plt.title('Погрешности численного решения')
plt.legend()
plt.grid(True)
plt.yscale('log')  # Логарифмическая шкала для лучшего отображения погрешностей

plt.tight_layout()
plt.show()

# Дополнительный график только с погрешностями (более детальный)
plt.figure(figsize=(10, 6))
plt.plot(t_num, error_x, 'b-', linewidth=2, label='Погрешность x(t)')
plt.plot(t_num, error_y, 'g-', linewidth=2, label='Погрешность y(t)')
plt.plot(t_num, error_z, 'r-', linewidth=2, label='Погрешность z(t)')
plt.xlabel('Время t')
plt.ylabel('Абсолютная погрешность')
plt.title('Погрешности численного решения методом Рунге-Кутты 4-го порядка')
plt.legend()
plt.grid(True)
plt.yscale('log')
plt.show()
