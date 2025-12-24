import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import root_scalar
from scipy.special import j0, j1


def model_parameters():
    params = {
        'I': 11,         # [Вт/м²]
        'C': 500,        # [Дж/(кг·К)]
        'rho': 7800,     # [кг/м³]
        'Rk': 0.12,      # [м]
        'T0': 20,        # [°C]
        't_max_hours': 3,
        'alpha': 100,    # [Вт/(м²·К)]
        'N_terms': 50,
        'lambda1': 12.0  # Вт/(м·К) - увеличенная теплопроводность
    }
    params['Bi'] = params['alpha'] * params['Rk'] / params['lambda1']
    params['a'] = params['lambda1'] / (params['C'] * params['rho'])
    params['a_fo'] = params['a'] / (params['Rk'] ** 2)
    return params


def eigen_eq(mu, Bi):
    return Bi * j0(mu) - mu * j1(mu)


def compute_eigenvalues(Bi, N_terms):
    mus = np.zeros(N_terms)
    for n in range(1, N_terms + 1):
        a_interval = max(1e-6, (n - 1) * np.pi)
        b_interval = n * np.pi
        sol = root_scalar(lambda mu: eigen_eq(mu, Bi), bracket=[a_interval, b_interval])
        mus[n - 1] = sol.root
    return mus


def compute_Ds(mus, Bi):
    Ds = np.zeros_like(mus)
    for i, mu in enumerate(mus):
        Ds[i] = 2 * Bi / ((mu ** 2 + Bi ** 2) * j0(mu))
    return Ds


def generate_time_vector(t_max_hours, num_points=2000):
    t_sec = np.linspace(0, t_max_hours * 3600, num_points)
    t_hours = t_sec / 3600
    return t_sec, t_hours


def V_temperature_vector(t_hours):
    V = np.zeros_like(t_hours)
    mask1 = t_hours <= 0.5
    mask2 = (t_hours > 0.5) & (t_hours <= 1.2)
    mask3 = (t_hours > 1.2) & (t_hours <= 1.5)
    mask4 = (t_hours > 1.5) & (t_hours <= 2.0)
    mask5 = t_hours > 2.0
    V[mask1] = 1600
    V[mask2] = 1200
    V[mask3] = 700
    V[mask4] = 1000
    V[mask5] = 500
    return V


def compute_temperature_cylinder(t_sec, r_rel, mus, Ds, T0, a_fo, V_array):
    tau_total = a_fo * t_sec
    T = np.zeros_like(tau_total)
    mu_sq = mus ** 2

    change_hours = np.array([0, 0.5, 1.2, 1.5, 2.0, 3.0]) * 3600
    change_times = np.searchsorted(t_sec, change_hours)

    for i, t_current in enumerate(t_sec):
        tau_current = tau_total[i]
        phi_total = 0

        for j in range(len(change_times) - 1):
            if change_times[j] >= len(t_sec) or t_sec[change_times[j]] > t_current:
                break

            tau_start = a_fo * t_sec[change_times[j]]
            tau_elapsed = tau_current - tau_start

            if j == 0:
                delta_V = V_array[0] - T0
            else:
                delta_V = V_array[change_times[j]] - V_array[change_times[j - 1]]

            if abs(delta_V) < 1e-6 or tau_elapsed <= 0:
                continue

            phi_step = np.sum(Ds * (1 - np.exp(-mu_sq * tau_elapsed)) * j0(mus * r_rel))
            phi_total += phi_step * delta_V

        T[i] = T0 + phi_total

    return T


def plot_temperatures(t_hours, T_center, T_surface, V_array, T_center_const, T_surface_const, t_max_hours, T0):
    fig, axes = plt.subplots(2, 1, figsize=(15, 10))

    # Переменная температура среды
    ax1 = axes[0]
    ax1.plot(t_hours, T_center, 'r-', linewidth=3, label='Центр цилиндра (r=0)')
    ax1.plot(t_hours, T_surface, 'b-', linewidth=3, label='Поверхность (r=R)')
    ax1.plot(t_hours, V_array, 'k--', linewidth=1.5, alpha=0.7, label='Температура среды V(t)')

    for point in [0.5, 1.2, 1.5, 2.0]:
        ax1.axvline(x=point, color='gray', linestyle=':', alpha=0.5)

    ax1.axhline(y=T0, color='gray', linestyle='-', alpha=0.5)
    ax1.set_xlabel('Время t, часы')
    ax1.set_ylabel('Температура T, °C')
    ax1.set_title('Температурные поля цилиндра при переменной температуре среды')
    ax1.legend(loc='upper right')
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(0, t_max_hours)
    ax1.set_ylim(T0 - 10, 1700)

    # Постоянная температура среды
    ax2 = axes[1]
    ax2.plot(t_hours, T_center_const, 'r-', linewidth=3, label='Центр цилиндра (r=0)')
    ax2.plot(t_hours, T_surface_const, 'b-', linewidth=3, label='Поверхность (r=R)')
    ax2.plot(t_hours, np.full_like(V_array, 1600), 'k--', linewidth=1.5, alpha=0.7, label='Температура среды V=1600°C')
    ax2.axhline(y=T0, color='gray', linestyle='-', alpha=0.5)
    ax2.set_xlabel('Время t, часы')
    ax2.set_ylabel('Температура T, °C')
    ax2.set_title('Температурные поля цилиндра при постоянной температуре среды (1600°C)')
    ax2.legend(loc='upper right')
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(0, t_max_hours)
    ax2.set_ylim(T0 - 10, 1700)

    plt.tight_layout()
    plt.show()


def analyze_results(params, t_hours, T_center, T_surface, T_center_const, T_surface_const, V_array):
    print("=" * 60)
    print("АНАЛИЗ РЕЗУЛЬТАТОВ:")
    print("=" * 60)
    print(f"Число Био: Bi = {params['Bi']:.2f}")
    print(f"Коэффициент температуропроводности: a = {params['a']:.2e} м²/с")
    print(f"Безразмерное время в конце: τ = {params['a_fo'] * params['t_max_hours']*3600:.4f}")

    idx_05h = np.searchsorted(t_hours, 0.5)
    idx_12h = np.searchsorted(t_hours, 1.2)

    print(f"\nТемпературы через 0.5 часа (при V=1600°C):")
    print(f"  Центр: {T_center_const[idx_05h]:.1f}°C")
    print(f"  Поверхность: {T_surface_const[idx_05h]:.1f}°C")

    print(f"\nТемпературы через 1.2 часа:")
    print(f"  Центр: {T_center[idx_12h]:.1f}°C (среда: {V_array[idx_12h]:.0f}°C)")
    print(f"  Поверхность: {T_surface[idx_12h]:.1f}°C (среда: {V_array[idx_12h]:.0f}°C)")

    print(f"\nМаксимальные температуры при переменной V(t):")
    print(f"  Центр: {np.max(T_center):.1f}°C в момент {t_hours[np.argmax(T_center)]:.2f} ч")
    print(f"  Поверхность: {np.max(T_surface):.1f}°C в момент {t_hours[np.argmax(T_surface)]:.2f} ч")

    print(f"\nМаксимальные температуры при постоянной V=1600°C:")
    print(f"  Центр: {np.max(T_center_const):.1f}°C")
    print(f"  Поверхность: {np.max(T_surface_const):.1f}°C")
    print("=" * 60)


def main():
    params = model_parameters()

    print(f"Число Био: Bi = {params['Bi']:.2f}")
    print(f"Коэффициент температуропроводности: a = {params['a']:.2e} м²/с")
    print(f"a_fo = {params['a_fo']:.2e} 1/с")

    mus = compute_eigenvalues(params['Bi'], params['N_terms'])
    Ds = compute_Ds(mus, params['Bi'])

    t_sec, t_hours = generate_time_vector(params['t_max_hours'])
    V_array = V_temperature_vector(t_hours)

    T_center = compute_temperature_cylinder(t_sec, 0, mus, Ds, params['T0'], params['a_fo'], V_array)
    T_surface = compute_temperature_cylinder(t_sec, 1, mus, Ds, params['T0'], params['a_fo'], V_array)

    # Постоянная V для сравнения
    V_const = np.full_like(V_array, 1600)
    T_center_const = compute_temperature_cylinder(t_sec, 0, mus, Ds, params['T0'], params['a_fo'], V_const)
    T_surface_const = compute_temperature_cylinder(t_sec, 1, mus, Ds, params['T0'], params['a_fo'], V_const)

    plot_temperatures(t_hours, T_center, T_surface, V_array, T_center_const, T_surface_const, params['t_max_hours'], params['T0'])
    analyze_results(params, t_hours, T_center, T_surface, T_center_const, T_surface_const, V_array)


if __name__ == "__main__":
    main()
