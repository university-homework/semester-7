import numpy as np
import matplotlib.pyplot as plt


def v_temperature_piecewise_array(t_seconds):
    t = np.asarray(t_seconds)

    scalar_input = False
    if t.ndim == 0:
        t = t.reshape(1)
        scalar_input = True

    v = np.full_like(t, 500.0, dtype=float)

    mask0 = (t >= 0) & (t < 3600)
    mask1 = (t >= 3600) & (t < 7200)
    mask2 = (t >= 7200) & (t < 9000)
    mask3 = (t >= 9000) & (t < 10800)

    tau_start = 600.0
    v[mask0] = 20.0 + (1600.0 - 20.0)*(1 - np.exp(-t[mask0]/tau_start))
    v[mask1] = 1200.0
    v[mask2] = 700.0
    v[mask3] = 1000.0

    if scalar_input:
        return v[0]
    return v


def solve_plate_CN(C, rho, L, T0, alpha, lambda_val, t_max, Nx=101, dt=1.0, theta=0.5):
    a = lambda_val / (C * rho)

    x = np.linspace(0.0, L, Nx)
    dx = x[1] - x[0]
    Nt = int(np.ceil(t_max / dt)) + 1
    time = np.linspace(0.0, t_max, Nt)

    T = np.full(Nx, T0, dtype=float)

    T_field = np.zeros((Nt, Nx), dtype=float)
    T_field[0, :] = T.copy()

    r = a * dt / dx ** 2

    A = np.zeros((Nx, Nx), dtype=float)
    B = np.zeros((Nx, Nx), dtype=float)
    for i in range(1, Nx - 1):
        A[i, i - 1] = -theta * r
        A[i, i] = 1.0 + 2.0 * theta * r
        A[i, i + 1] = -theta * r

        B[i, i - 1] = (1.0 - theta) * r
        B[i, i] = 1.0 - 2.0 * (1.0 - theta) * r
        B[i, i + 1] = (1.0 - theta) * r

    A0_diag = 1.0 + 2.0 * theta * r + 2.0 * theta * (a * dt) * (alpha / (lambda_val * dx))
    A[0, 0] = A0_diag
    A[0, 1] = -2.0 * theta * r

    B0_diag = 1.0 - 2.0 * (1.0 - theta) * r - 2.0 * (1.0 - theta) * (a * dt) * (alpha / (lambda_val * dx))
    B[0, 0] = B0_diag
    B[0, 1] = 2.0 * (1.0 - theta) * r

    rhs_v_coeff_A = 2.0 * theta * (a * dt) * (alpha / (lambda_val * dx))
    rhs_v_coeff_B = 2.0 * (1.0 - theta) * (a * dt) * (alpha / (lambda_val * dx))

    i = Nx - 1
    A[i, i] = 1.0 + 2.0 * theta * r
    A[i, i - 1] = -2.0 * theta * r
    B[i, i] = 1.0 - 2.0 * (1.0 - theta) * r
    B[i, i - 1] = 2.0 * (1.0 - theta) * r

    for n in range(1, Nt):
        t_n = time[n - 1]
        t_np1 = time[n]
        v_n = v_temperature_piecewise_array(t_n)
        v_np1 = v_temperature_piecewise_array(t_np1)

        rhs = B.dot(T)
        rhs[0] += rhs_v_coeff_B * v_n + rhs_v_coeff_A * v_np1

        T_new = np.linalg.solve(A, rhs)
        T = T_new
        T_field[n, :] = T.copy()

    v_time = v_temperature_piecewise_array(time)
    T_surface = T_field[:, 0]
    T_center = T_field[:, Nx // 2]
    return time, x, T_field, T_surface, T_center, v_time


def main():
    C = 368.0  # Дж/(кг·°C)
    rho = 8130.0  # кг/м^3
    L = 0.12  # м (толщина пластины / характерная глубина)
    T0 = 20.0  # °C
    alpha = 200.0  # Вт/(м^2·°C)
    lambda_val = 2.3 * 11.0  # Вт/(м·°C)
    t_max = 3.0 * 3600.0  # 3.5 часа в секундах

    Nx = 201
    dt = 2.0

    time, x, T_field, T_surface, T_center, v_time = solve_plate_CN(
        C, rho, L, T0, alpha, lambda_val, t_max, Nx=Nx, dt=dt, theta=0.5
    )

    print("ПАРАМЕТРЫ РАСЧЕТА:")
    print(f"Длина L = {L} м")
    print(f"Начальная температура T0 = {T0} °C")
    print(f"Коэффициент теплопроводности λ = {lambda_val} Вт/(м·°C)")
    print(f"Коэффициент теплоотдачи α = {alpha} Вт/(м²·°C)")
    print(f"Число Био Bi = αL/λ = {alpha * L / lambda_val:.3f}")

    a = lambda_val / (C * rho)
    print(f"Коэффициент температуропроводности a = {a:.6e} м²/с")
    print(f"Характерное время нагрева L²/a = {L ** 2 / a / 3600:.2f} часов")

    print(f"\nРЕЗУЛЬТАТЫ:")
    print(f"Максимальная температура поверхности: {np.max(T_surface):.2f} °C")
    print(f"Максимальная температура в центре: {np.max(T_center):.2f} °C")
    print(f"Максимальная разность (поверхность - центр): {np.max(T_surface - T_center):.2f} °C")


    plt.figure(figsize=(10, 6))

    plt.plot(time / 3600.0, T_surface, 'r-', label='Температура поверхности', linewidth=2.5)
    plt.plot(time / 3600.0, T_center, 'b-', label='Температура центра', linewidth=2.5)

    for t_h in [1, 2, 2.5, 3]:
        plt.axvline(x=t_h, color='gray', linestyle=':', alpha=0.5)

    intervals = [(0, 0.5, 1600), (0.5, 1.2, 1200), (1.2, 1.5, 700),
                 (1.5, 2.0, 1000), (2.0, 3.0, 500)]
    for start, end, temp in intervals:
        plt.text((start + end) / 2, temp + 100, f'{temp}°C',
                 ha='center', va='bottom', fontsize=10, alpha=0.8,
                 bbox=dict(boxstyle='round,pad=0.2', facecolor='yellow', alpha=0.3))

    plt.xlabel('Время, ч', fontsize=12)
    plt.ylabel('Температура, °C', fontsize=12)
    plt.title('Нагрев пластины', fontsize=14, pad=15)
    plt.legend(loc='upper right', fontsize=11)
    plt.grid(alpha=0.3)
    plt.ylim(0, 1800)
    plt.xlim(0, 3.0)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
