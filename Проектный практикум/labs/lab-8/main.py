import numpy as np
import matplotlib.pyplot as plt

# Функции
def x_func(t):
    return (4 - t**2) / (1 + t**3)

def y_func(t):
    return (t**2) / (1 + t**3)

# Диапазон параметра t
t = np.linspace(-4, 4, 2000)  # избегаем точки t = -1 (деление на ноль)

x = x_func(t)
y = y_func(t)

# Создаём фигуру
plt.figure(figsize=(8, 6))

# Основные линии сетки
plt.grid(True, which='major', linewidth=0.8, color='gray')

# Вспомогательные линии сетки
plt.grid(True, which='minor', linestyle='--', linewidth=0.5, color='lightgray')

plt.axhline(0, color='black', linewidth=2)  # ось X
plt.axvline(0, color='black', linewidth=2)  # ось Y

plt.minorticks_on()
plt.ylim(-2, 4)

# График
plt.plot(t, x, label=r"$x(t)=\frac{4-t^2}{1+t^3}$", color="blue")
plt.plot(t, y, label=r"$y(t)=\frac{t^2}{1+t^3}$", color="red")

# Название
plt.title("Графики функций x(t) и y(t)")

# Оси
plt.xlabel("t")
plt.ylabel("Значение функции")

# Математическая подпись
plt.legend()

# Автоматическое сохранение в SVG
output_file = "functions_plot.svg"
plt.savefig(output_file, format="svg")

plt.show()

print("SVG график сохранён в файл:", output_file)
