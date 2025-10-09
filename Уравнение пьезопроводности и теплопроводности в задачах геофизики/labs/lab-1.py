import numpy as np
import matplotlib.pyplot as plt


def f(t, x, y):
    return y


def g(t, x, y):
    return 11


def exact_solution(t):
    x_exact = (11 * t ** 2) / 2 + t + 1
    y_exact = 11 * t + 1
    return x_exact, y_exact


def runge_kutta_system(t_span, x0, y0, n_steps):
    t0, t_n = t_span
    h = (t_n - t0) / n_steps
    t = np.zeros(n_steps + 1)
    x = np.zeros(n_steps + 1)
    y = np.zeros(n_steps + 1)

    t[0] = t0
    x[0] = x0
    y[0] = y0

    for i in range(n_steps):
        # Коэффициенты для первого уравнения (dx/dt = y)
        k1 = f(t[i], x[i], y[i])
        p1 = g(t[i], x[i], y[i])

        k2 = f(t[i] + h / 2, x[i] + (h / 2) * k1, y[i] + (h / 2) * p1)
        p2 = g(t[i] + h / 2, x[i] + (h / 2) * k1, y[i] + (h / 2) * p1)

        k3 = f(t[i] + h / 2, x[i] + (h / 2) * k2, y[i] + (h / 2) * p2)
        p3 = g(t[i] + h / 2, x[i] + (h / 2) * k2, y[i] + (h / 2) * p2)

        k4 = f(t[i] + h, x[i] + h * k3, y[i] + h * p3)
        p4 = g(t[i] + h, x[i] + h * k3, y[i] + h * p3)

        x[i + 1] = x[i] + (h / 6) * (k1 + 2 * k2 + 2 * k3 + k4)
        y[i + 1] = y[i] + (h / 6) * (p1 + 2 * p2 + 2 * p3 + p4)
        t[i + 1] = t[i] + h

    return t, x, y


# Параметры
t_span = (0, 5)
x0 = 1
y0 = 1
n_steps = 500

# Численное решение
t_num, x_rk4, y_rk4 = runge_kutta_system(t_span, x0, y0, n_steps)

# Аналитическое решение
t_analytical = np.linspace(0, 5, 1000)
x_exact, y_exact = exact_solution(t_analytical)

# Вывод результатов
print("Сравнение решений в конечной точке t=5:")
print(f"x_численное = {x_rk4[-1]:.8f}")
print(f"x_аналитическое = {exact_solution(5)[0]:.8f}")
print(f"Погрешность x = {abs(x_rk4[-1] - exact_solution(5)[0]):.2e}")

print(f"\ny_численное = {y_rk4[-1]:.8f}")
print(f"y_аналитическое = {exact_solution(5)[1]:.8f}")
print(f"Погрешность y = {abs(y_rk4[-1] - exact_solution(5)[1]):.2e}")

# Создаем 4 отдельных графика
plt.figure(figsize=(15, 10))

# График 1: Численное решение для x(t)
plt.subplot(2, 2, 1)
plt.plot(t_num, x_rk4, 'b-', linewidth=2)
plt.xlabel('Время t')
plt.ylabel('x(t)')
plt.title('Численное решение для x(t)')
plt.grid(True)

# График 2: Аналитическое решение для x(t)
plt.subplot(2, 2, 2)
plt.plot(t_analytical, x_exact, 'r-', linewidth=2)
plt.xlabel('Время t')
plt.ylabel('x(t)')
plt.title('Аналитическое решение для x(t)')
plt.grid(True)

# График 3: Численное решение для y(t)
plt.subplot(2, 2, 3)
plt.plot(t_num, y_rk4, 'g-', linewidth=2)
plt.xlabel('Время t')
plt.ylabel('y(t)')
plt.title('Численное решение для y(t)')
plt.grid(True)

# График 4: Аналитическое решение для y(t)
plt.subplot(2, 2, 4)
plt.plot(t_analytical, y_exact, 'm-', linewidth=2)
plt.xlabel('Время t')
plt.ylabel('y(t)')
plt.title('Аналитическое решение для y(t)')
plt.grid(True)

plt.tight_layout()
plt.show()

# Дополнительные графики для сравнения и погрешностей
plt.figure(figsize=(15, 10))

# График 5: Сравнение численного и аналитического решения для x(t)
plt.subplot(2, 2, 1)
plt.plot(t_num, x_rk4, 'b-', linewidth=2, label='Численное')
plt.plot(t_analytical, x_exact, 'r--', linewidth=1, label='Аналитическое')
plt.xlabel('Время t')
plt.ylabel('x(t)')
plt.title('Сравнение решений для x(t)')
plt.legend()
plt.grid(True)

# График 6: Сравнение численного и аналитического решения для y(t)
plt.subplot(2, 2, 2)
plt.plot(t_num, y_rk4, 'g-', linewidth=2, label='Численное')
plt.plot(t_analytical, y_exact, 'm--', linewidth=1, label='Аналитическое')
plt.xlabel('Время t')
plt.ylabel('y(t)')
plt.title('Сравнение решений для y(t)')
plt.legend()
plt.grid(True)

# График 7: Погрешность для x(t)
plt.subplot(2, 2, 3)
error_x = [abs(x_rk4[i] - exact_solution(t_num[i])[0]) for i in range(len(t_num))]
plt.plot(t_num, error_x, 'r-', linewidth=1)
plt.xlabel('Время t')
plt.ylabel('Погрешность')
plt.title('Погрешность для x(t)')
plt.grid(True)

# График 8: Погрешность для y(t)
plt.subplot(2, 2, 4)
error_y = [abs(y_rk4[i] - exact_solution(t_num[i])[1]) for i in range(len(t_num))]
plt.plot(t_num, error_y, 'm-', linewidth=1)
plt.xlabel('Время t')
plt.ylabel('Погрешность')
plt.title('Погрешность для y(t)')
plt.grid(True)

plt.tight_layout()
plt.show()
