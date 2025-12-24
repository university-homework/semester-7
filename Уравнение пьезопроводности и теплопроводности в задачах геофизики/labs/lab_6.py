import numpy as np
import warnings
import plotly.graph_objects as go

warnings.filterwarnings('ignore')

T_0 = 5  # Начальная температура, °C
T_C = 28  # Температура нагрева, °C
R_w = 0.05  # Радиус скважины, м
R_K = 200  # Радиус пласта, м
t_max = 100  # Время нагрева, сутки
a_SK = 0.0044  # Теплопроводность, м²/ч


def physical_heating_model(t_days, position, R_K):
    """Вычисляет температуру в зависимости от времени и позиции."""
    a_SK_si = a_SK / 3600  # м²/с

    if position == 'surface':
        tau_s = R_w**2 / a_SK_si / (24*3600)
        heating_factor = 1 - np.exp(-t_days / tau_s)
    elif position == 'center':
        distance_to_center = R_K / 2
        tau_c = (distance_to_center**2) / a_SK_si / (24*3600)
        heating_factor = np.tanh(np.sqrt(t_days / tau_c))
    else:
        raise ValueError("Position must be 'surface' or 'center'")

    return T_0 + heating_factor * (T_C - T_0)


def generate_time_points(t_max):
    """Генерирует логарифмически распределённые временные точки для расчёта температур."""
    t_days = np.unique(np.concatenate([
        np.logspace(-6, -3, 100),
        np.logspace(-3, -1, 200),
        np.logspace(-1, 0, 150),
        np.logspace(0, 1, 200),
        np.logspace(1, np.log10(50), 200),
        np.logspace(np.log10(50), np.log10(t_max), 1000)
    ]))
    return t_days


def plot_temperatures(t_days, T_surface, T_center):
    """Интерактивный график температур с подсказками при наведении."""

    fig = go.Figure()

    # Линия поверхности скважины
    fig.add_trace(go.Scatter(
        x=t_days, y=T_surface,
        mode='lines+markers',
        name='Поверхность скважины',
        line=dict(color='#FF6F61', width=2),
        hovertemplate='t=%{x:.4f} сут<br>T=%{y:.2f}°C<extra></extra>'
    ))

    # Линия центра пласта
    fig.add_trace(go.Scatter(
        x=t_days, y=T_center,
        mode='lines+markers',
        name='Центр пласта',
        line=dict(color='#6B5B95', width=2),
        hovertemplate='t=%{x:.4f} сут<br>T=%{y:.2f}°C<extra></extra>'
    ))

    # Заливка между линиями
    fig.add_trace(go.Scatter(
        x=np.concatenate([t_days, t_days[::-1]]),
        y=np.concatenate([T_surface, T_center[::-1]]),
        fill='toself',
        fillcolor='rgba(136,176,75,0.2)',
        line=dict(color='rgba(255,255,255,0)'),
        hoverinfo='skip',
        showlegend=True,
        name='Разница температур'
    ))

    # Масштаб оси X логарифмический
    fig.update_xaxes(type="log", title_text='Время нагрева, сутки', range=[-4, np.log10(t_days[-1])])
    fig.update_yaxes(title_text='Температура, °C', range=[T_0 - 1, T_C + 1])

    fig.update_layout(
        title='Прогрев скважины и центра пласта',
        legend=dict(x=0.7, y=0.05),
        width=900, height=600
    )

    fig.show()


def print_temperature_table(t_days, T_surface, T_center, t_max):
    """Выводит таблицу прогрева центра и поверхности."""
    print(f"{'Время, сут':<15} {'Темп. пов.':<15} {'Темп. центр':<15} {'Разница':<15} {'Прогрев центра, %':<15}")
    print("-" * 80)

    time_checkpoints = np.logspace(np.log10(0.0001), np.log10(t_max), 20)
    time_checkpoints = [t for t in time_checkpoints if t <= t_max]

    for t_point in time_checkpoints:
        idx = np.argmin(np.abs(t_days - t_point))
        diff = T_surface[idx] - T_center[idx]
        center_progress = 100 * (T_center[idx] - T_0) / (T_C - T_0)
        print(f"{t_point:<15.4f} {T_surface[idx]:<15.2f} {T_center[idx]:<15.4f} {diff:<15.2f} {center_progress:<14.2f}")


def calculate_characteristic_time_center(R_K):
    """Вычисляет характерное время прогрева центра пласта, сут."""
    a_SK_si = a_SK / 3600
    tau_center_s = (R_K / 2)**2 / a_SK_si
    tau_center_days = tau_center_s / (24*3600)
    return tau_center_days


def main():
    print(f"Начальная температура: {T_0}°C")
    print(f"Температура нагрева: {T_C}°C")
    print(f"Радиус скважины: R_w = {R_w} м")
    print(f"Радиус пласта: R_K = {R_K} м")
    print(f"Отношение R_K/R_w = {R_K/R_w:.0f}")
    print(f"Время нагрева: {t_max} суток\n")

    t_days = generate_time_points(t_max)
    T_surface = physical_heating_model(t_days, 'surface', R_K)
    T_center = physical_heating_model(t_days, 'center', R_K)

    print("Температура в начале (t≈0):")
    print(f"Поверхность: {T_surface[0]:.6f}°C")
    print(f"Центр: {T_center[0]:.6f}°C\n")

    plot_temperatures(t_days, T_surface, T_center)
    print_temperature_table(t_days, T_surface, T_center, t_max)

    tau_center_days = calculate_characteristic_time_center(R_K)
    print(f"\nХарактерное время прогрева центра пласта: {tau_center_days:.2f} суток")


if __name__ == "__main__":
    main()
