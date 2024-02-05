import pyrealsense2 as rs
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


# Функция для установки заголовков, подписей и пределов осей
def set_labels_and_titles(ax, title, xlabel, ylabel, zlabel=None):
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    limit = (-5, 5)
    ax.set_xlim(limit)
    ax.set_ylim(limit)
    if zlabel and hasattr(ax, 'set_zlabel'):
        ax.set_zlabel(zlabel)
        ax.set_zlim(limit)

# Настроим контекст потока
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.pose)

# Запустим поток с нашими настройками
pipeline.start(config)

# Настроим макет графиков
fig = plt.figure(figsize=(15, 12))  
gs = gridspec.GridSpec(2, 4, height_ratios=[2, 1], width_ratios=[1, 1, 1, 0.1], hspace=0.8, wspace=1.5)

# Создадим четыре графика
ax1 = fig.add_subplot(gs[0, 0:3], projection='3d')  # 3D график
ax2 = fig.add_subplot(gs[1, 0])  # Вид сверху
ax3 = fig.add_subplot(gs[1, 1])  # Вид сбоку
ax4 = fig.add_subplot(gs[1, 2])  # Вид спереди

# Добавим подписи, заголовки и пределы осей
set_labels_and_titles(ax1, '3D Трекинг', 'X', 'Y', 'Z')
set_labels_and_titles(ax2, 'Вид сверху', 'X', 'Y')
set_labels_and_titles(ax3, 'Вид сбоку', 'X', 'Z')
set_labels_and_titles(ax4, 'Вид спереди', 'Y', 'Z')

x, y, z = [], [], []

try:
    while True:
        frames = pipeline.wait_for_frames()
        pose_frame = frames.get_pose_frame()
        if pose_frame:
            data = pose_frame.get_pose_data()
            x.append(data.translation.z)
            y.append(data.translation.x)
            z.append(data.translation.y)

            # Очищаем графики
            ax1.clear()
            ax2.clear()
            ax3.clear()
            ax4.clear()

            # Перерисовываем графики
            ax1.scatter(x, y, z, c='r', marker='o')
            ax2.scatter(x, y, c='g', marker='o')
            ax3.scatter(x, z, c='b', marker='o')
            ax4.scatter(y, z, c='y', marker='o')

            # Первую точку отметим символом 'x'
            marker_size = 100  # Размер маркера
            if len(x) > 0:
                ax1.scatter(x[0], y[0], z[0], c='k', marker='x', s=marker_size)
                ax2.scatter(x[0], y[0], c='k', marker='x', s=marker_size)
                ax3.scatter(x[0], z[0], c='k', marker='x', s=marker_size)
                ax4.scatter(y[0], z[0], c='k', marker='x', s=marker_size)

            # Восстановление подписей, заголовков и пределов осей после очистки
            set_labels_and_titles(ax1, '3D Трекинг', 'X', 'Y', 'Z')
            set_labels_and_titles(ax2, 'Вид сверху', 'X', 'Y')
            set_labels_and_titles(ax3, 'Вид сбоку', 'X', 'Z')
            set_labels_and_titles(ax4, 'Вид спереди', 'Y', 'Z')

            plt.pause(0.05)

except KeyboardInterrupt:
    print("Завершено пользователем")
finally:
    pipeline.stop()
