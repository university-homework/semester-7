import numpy as np
import matplotlib.pyplot as plt


def chemical_system(t, variables, k1, k2):
    """
    Система дифференциальных уравнений для последовательной реакции X → Y → Z
    """
    x, y, z = variables
    dxdt = -k1 * x
    dydt = k1 * x - k2 * y
    dzdt = k2 * y
    return np.array([dxdt, dydt, dzdt])


def analytical_solution(t, k1, k2, x0):
    """
    Аналитическое решение для системы X → Y → Z
    """
    x_analytical = x0 * np.exp(-k1 * t)

    if k1 == k2:
        y_analytical = x0 * k1 * t * np.exp(-k1 * t)
    else:
        y_analytical = x0 * k1 / (k2 - k1) * (np.exp(-k1 * t) - np.exp(-k2 * t))

    z_analytical = x0 - x_analytical - y_analytical

    return x_analytical, y_analytical, z_analytical


def runge_kutta_4th_order(ode_system, t_span, initial_conditions, parameters, n_steps=1000):
    """
    Реализация метода Рунге-Кутты 4-го порядка для решения систем ОДУ
    """
    t_start, t_end = t_span
    t = np.linspace(t_start, t_end, n_steps)
    step_size = t[1] - t[0]

    # Инициализация массива решений
    solution = np.zeros((n_steps, len(initial_conditions)))
    solution[0] = initial_conditions

    # Численное интегрирование
    for i in range(n_steps - 1):
        k1 = step_size * ode_system(t[i], solution[i], *parameters)
        k2 = step_size * ode_system(t[i] + step_size / 2, solution[i] + k1 / 2, *parameters)
        k3 = step_size * ode_system(t[i] + step_size / 2, solution[i] + k2 / 2, *parameters)
        k4 = step_size * ode_system(t[i] + step_size, solution[i] + k3, *parameters)

        solution[i + 1] = solution[i] + (k1 + 2 * k2 + 2 * k3 + k4) / 6

    return t, solution


def plot_solutions_and_errors(time, concentrations, analytical, parameters):
    """
    Построение графиков концентраций и погрешностей
    """
    x_num, y_num, z_num = concentrations
    x_anal, y_anal, z_anal = analytical

    # Вычисление абсолютных погрешностей (модуль разности)
    abs_error_x = np.abs(x_num - x_anal)
    abs_error_y = np.abs(y_num - y_anal)
    abs_error_z = np.abs(z_num - z_anal)

    # Создаем subplots (2 графика в ряд)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    # График 1: Концентрации всех веществ (численные vs аналитические)
    ax1.plot(time, x_num, 'b-', linewidth=2, label='X(t) - численное')
    ax1.plot(time, y_num, 'r-', linewidth=2, label='Y(t) - численное')
    ax1.plot(time, z_num, 'g-', linewidth=2, label='Z(t) - численное')
    ax1.plot(time, x_anal, 'b--', alpha=0.7, linewidth=1, label='X(t) - аналитическое')
    ax1.plot(time, y_anal, 'r--', alpha=0.7, linewidth=1, label='Y(t) - аналитическое')
    ax1.plot(time, z_anal, 'g--', alpha=0.7, linewidth=1, label='Z(t) - аналитическое')

    ax1.set_xlabel('Время', fontsize=12)
    ax1.set_ylabel('Концентрация', fontsize=12)
    ax1.set_title('Концентрации веществ\n(численные vs аналитические решения)', fontsize=13)
    ax1.legend(fontsize=10, loc='best')
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(0, 20)

    # График 2: Абсолютные погрешности всех веществ на одном графике
    ax2.plot(time, abs_error_x, 'b-', linewidth=1.5, label=f'|ΔX| (макс: {np.max(abs_error_x):.2e})')
    ax2.plot(time, abs_error_y, 'r-', linewidth=1.5, label=f'|ΔY| (макс: {np.max(abs_error_y):.2e})')
    ax2.plot(time, abs_error_z, 'g-', linewidth=1.5, label=f'|ΔZ| (макс: {np.max(abs_error_z):.2e})')
    ax2.axhline(y=0, color='k', linestyle='-', alpha=0.3)

    ax2.set_xlabel('Время', fontsize=12)
    ax2.set_ylabel('Абсолютная погрешность', fontsize=12)
    ax2.set_title('Абсолютные погрешности всех веществ', fontsize=13)
    ax2.legend(fontsize=10, loc='best')
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(0, 20)

    # Масштабирование по y для графика погрешностей
    max_abs_error = max(np.max(abs_error_x), np.max(abs_error_y), np.max(abs_error_z))
    ax2.set_ylim(0, max_abs_error * 1.1)

    # Улучшаем читаемость числовых меток на оси Y
    from matplotlib.ticker import ScalarFormatter
    ax2.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
    ax2.ticklabel_format(axis='y', style='sci', scilimits=(-2, 2))

    plt.suptitle(f'Последовательная реакция X → Y → Z: k1 = {parameters[0]}, k2 = {parameters[1]}',
                 fontsize=14, y=1.02)
    plt.tight_layout()
    plt.show()

    return abs_error_x, abs_error_y, abs_error_z


def print_error_statistics(time, errors, names):
    """
    Вывод статистики погрешностей
    """
    print("=" * 60)
    print("СТАТИСТИКА АБСОЛЮТНЫХ ПОГРЕШНОСТЕЙ (|численное - аналитическое|)")
    print("=" * 60)

    for error, name in zip(errors, names):
        max_error = np.max(error)
        rms_error = np.sqrt(np.mean(error ** 2))
        mean_error = np.mean(error)
        std_error = np.std(error)

        print(f"{name}:")
        print(f"  Максимальная абсолютная погрешность: {max_error:.2e}")
        print(f"  Среднеквадратичная погрешность:       {rms_error:.2e}")
        print(f"  Средняя абсолютная погрешность:      {mean_error:.2e}")
        print(f"  Стандартное отклонение:              {std_error:.2e}")
        print()


def solve_chemical_kinetics():
    """
    Основная функция решения задачи химической кинетики
    """
    # Параметры модели
    reaction_constants = (0.2, 0.8)  # k1, k2
    time_span = (0, 20)  # начальное и конечное время
    initial_concentrations = [100, 0, 0]  # x0, y0, z0
    number_of_steps = 1000

    print("Решение системы дифференциальных уравнений...")
    print(f"Параметры: k1 = {reaction_constants[0]}, k2 = {reaction_constants[1]}")
    print(f"Временной интервал: {time_span[0]} - {time_span[1]}")
    print(f"Количество шагов: {number_of_steps}")

    # Решение системы уравнений численным методом
    time, solution = runge_kutta_4th_order(
        chemical_system,
        time_span,
        initial_concentrations,
        reaction_constants,
        number_of_steps
    )

    # Аналитическое решение
    x_anal, y_anal, z_anal = analytical_solution(time, reaction_constants[0], reaction_constants[1],
                                                 initial_concentrations[0])

    # Извлечение численных решений
    concentrations = (
        solution[:, 0],  # X(t)
        solution[:, 1],  # Y(t)
        solution[:, 2]  # Z(t)
    )

    analytical_concentrations = (x_anal, y_anal, z_anal)

    # Визуализация и расчет абсолютных погрешностей
    abs_errors = plot_solutions_and_errors(time, concentrations, analytical_concentrations, reaction_constants)

    # Вывод статистики
    print_error_statistics(time, abs_errors, ['|ΔX(t)|', '|ΔY(t)|', '|ΔZ(t)|'])

    # Проверка сохранения массы для численного решения
    total_mass_numerical = concentrations[0] + concentrations[1] + concentrations[2]
    mass_error = np.abs(total_mass_numerical - sum(initial_concentrations))
    print(f"Сохранение массы (численное решение):")
    print(f"  Максимальное отклонение: {np.max(mass_error):.2e}")
    print(f"  Среднее отклонение:      {np.mean(mass_error):.2e}")

    return time, concentrations, analytical_concentrations, abs_errors


if __name__ == "__main__":
    # Запуск расчета
    time, concentrations, analytical, errors = solve_chemical_kinetics()