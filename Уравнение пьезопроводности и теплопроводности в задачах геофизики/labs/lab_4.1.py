import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

C = 368  # Дж/(кг·°C)
rho = 8130  # кг/м³
R = 0.12  # м
T0 = 20  # °C
alpha = 200  # Вт/(м²·°C)
lambda_val = 2.3 * 11  # Вт/(м·°C)
t_max = 10 * 3600  # сек

T_target = 1600  # °C

print(f"Расчет для температуры среды: {T_target}°C")

Bi = alpha * R / lambda_val
print(f"Bi = {Bi:.3f}")


def equation(mu, Bi):
    return Bi * np.cos(mu) - mu * np.sin(mu)


N_roots = 10
mu_roots = []
for n in range(1, N_roots + 1):
    guess = (n - 0.5) * np.pi if n == 1 else mu_roots[-1] + np.pi
    mu_n = fsolve(equation, guess, args=(Bi))[0]
    mu_roots.append(mu_n)
mu_roots = np.array(mu_roots)

print("Первые 6 корней:")
for i, mu in enumerate(mu_roots[:6], 1):
    print(f"μ_{i} = {mu:.6f}")

D_n = 2 * Bi ** 2 / (mu_roots * (mu_roots ** 2 + Bi ** 2 + Bi)) / np.sin(mu_roots)


def v_temperature(t):
    return T0 + (T_target - T0) * (1 - np.exp(-t / 600))


def solve_temperature_optimized(N_terms=10):
    time_points = np.linspace(0, t_max, 500)

    a = lambda_val / (C * rho)
    Fo_points = a * time_points / R ** 2
    v_temp_points = v_temperature(time_points)

    dv_dt = np.zeros_like(time_points)
    dv_dt[1:] = (v_temp_points[1:] - v_temp_points[:-1]) / (time_points[1:] - time_points[:-1])
    dv_dt[0] = dv_dt[1]

    T_center = np.zeros_like(time_points)
    T_surface = np.zeros_like(time_points)

    exp_matrix = np.zeros((N_terms, len(time_points), len(time_points)))

    for n in range(N_terms):
        for i in range(len(time_points)):
            for j in range(i, len(time_points)):
                exp_matrix[n, i, j] = np.exp(-mu_roots[n] ** 2 * (Fo_points[j] - Fo_points[i]))

    for idx in range(len(time_points)):
        if time_points[idx] == 0:
            T_center[idx] = T0
            T_surface[idx] = T0
            continue

        sum_center = 0
        sum_surface = 0

        for n in range(N_terms):
            integral = 0
            for i in range(1, idx + 1):
                dt = time_points[i] - time_points[i - 1]
                integral += dv_dt[i] * exp_matrix[n, i, idx] * dt

            sum_center += D_n[n] * integral
            sum_surface += D_n[n] * np.cos(mu_roots[n]) * integral

        T_center[idx] = v_temp_points[idx] - sum_center
        T_surface[idx] = v_temp_points[idx] - sum_surface

    return time_points, T_center, T_surface


time, T_center, T_surface = solve_temperature_optimized(N_terms=6)

plt.figure(figsize=(12, 6))
plt.plot(time / 3600, T_center, 'b-', linewidth=2, label='Температура в центре')
plt.plot(time / 3600, T_surface, 'r-', linewidth=2, label='Температура на поверхности')
plt.xlabel('Время, ч')
plt.ylabel('Температура, °C')
plt.title(f'Нагрев до {T_target}°C')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

diff = T_surface - T_center
print(f"Максимальная температура поверхности: {np.max(T_surface):.1f}°C")
print(f"Максимальная температура центра: {np.max(T_center):.1f}°C")
print(f"Максимальная разность температур: {np.max(diff):.1f}°C")
