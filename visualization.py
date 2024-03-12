import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import gridspec

def tracking_visualization(data):
    x = data[:,2]
    y = data[:,0]
    z = data[:,1]

    offset_limit = 0.5
    # Определение пределов для осей, чтобы обеспечить одинаковые подписи и отрезки
    x_min, x_max = min(x)-offset_limit, max(x)+offset_limit
    y_min, y_max = min(y)-offset_limit, max(y)+offset_limit
    z_min, z_max = min(y)-offset_limit, max(y)+offset_limit

    # Создаем фигуру и грид для сабплотов
    fig = plt.figure(figsize=(16, 8))
    gs = gridspec.GridSpec(2, 3, height_ratios=[2, 1])

    # 3D график в верхней части
    ax1 = fig.add_subplot(gs[0, :], projection='3d')
    ax1.scatter(x, y, z, c='r', marker='o')
    ax1.set_title('3D View')
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    ax1.set_zlabel('Z')

    # Функция для установления одинаковых пределов и аспекта для 2D-графиков
    def set_square_aspect_and_limits(ax, xlim, ylim):
        ax.set_aspect(aspect='equal', adjustable='box')
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)

    # Вид сверху
    ax2 = fig.add_subplot(gs[1, 0])
    ax2.scatter(x, y, c='g', marker='o')
    ax2.set_title('Вид сверху (XY)')
    ax2.set_xlabel('X')
    ax2.set_ylabel('Y')
    set_square_aspect_and_limits(ax2, (x_min, x_max), (y_min, y_max))

    # Вид сбоку 
    ax3 = fig.add_subplot(gs[1, 1])
    ax3.scatter(x, z, c='b', marker='o')
    ax3.set_title('Вид сбоку (XZ)')
    ax3.set_xlabel('X')
    ax3.set_ylabel('Z')
    set_square_aspect_and_limits(ax3, (x_min, x_max), (z_min, z_max))

    # Вид спереди (YZ) в нижней части справа
    ax4 = fig.add_subplot(gs[1, 2])
    ax4.scatter(y, z, c='y', marker='o')
    ax4.set_title('Вид спереди (YZ)')
    ax4.set_xlabel('Y')
    ax4.set_ylabel('Z')
    set_square_aspect_and_limits(ax4, (y_min, y_max), (z_min, z_max))

    plt.tight_layout()
    plt.show()


def comparison_subplot(original_data, filtered_datas, labels, x_label):

    fig, axs = plt.subplots(2, 3, figsize=(15, 10))  # Создаем сетку графиков: 2 строки на 3 столбца
    fig.tight_layout(pad=5.0)
    
    # Создаем графики в цикле
    for i, (filtered_data, label) in enumerate(zip(filtered_datas, labels)):
        row, col = divmod(i, 3)  # Определяем позицию графика в сетке
        axs[row, col].plot(original_data, label='Без фильтра', linestyle='--', linewidth=2)
        axs[row, col].plot(filtered_data, label=f'{label}')
        axs[row, col].set_title(f'{label}')
        axs[row, col].set_xlabel(x_label)
        axs[row, col].set_ylabel('Значения')
        axs[row, col].legend()
    
    # Убираем последний (шестой) график, так как он нам не нужен
    fig.delaxes(axs[1][2])
    
    plt.show()