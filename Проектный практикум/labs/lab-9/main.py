import numpy as np
import matplotlib.pyplot as plt

# Параметры
h = np.pi / 16
phi = np.arange(-np.pi/2, np.pi/2 + h, h)

# Функция
p = 3 * np.cos(phi)

# Создаем рисунок
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='polar')

# Основная сетка
ax.grid(True, which='major', linewidth=0.8, color='gray')

# Вспомогательная сетка (меньшая)
ax.grid(True, which='minor', linestyle='--', linewidth=0.5, color='lightgray')

# Включаем минорные деления (по углу)
ax.set_rmin(5)

# График функции
ax.plot(phi, p, label=r"$p = 3\cos(\varphi)$", color="blue", linewidth=2)

# Название графика
plt.title("Полярный график: p = 3cos(φ)", fontsize=14)

# Математическая запись функции (легенда)
plt.legend(loc="upper right")

# Сохранение в SVG
output_file = "polar_plot.svg"
plt.savefig(output_file, format="svg")

plt.show()

print("SVG файл сохранён как:", output_file)
