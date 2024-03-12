import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from memory_profiler import memory_usage
import cProfile
import pstats
import io

from filters import moving_average_filter, median_filter, kalman_filter, gaussian_filter, savitzky_golay_filter
from visualization import tracking_visualization, comparison_subplot

# Профилирование: время
def profile_function(data):
    pr = cProfile.Profile()
    pr.enable()      
    filtered_data = savitzky_golay_filter(data) # менять функцию фильтра
    pr.disable() 
    s = io.StringIO()
    sortby = 'cumulative'  # Сортировка по общему времени, затраченному в функции и всех вызываемых ею функциях
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    
    return filtered_data, s.getvalue()

# Профилирование: память
def profile_memory(data):
    # Использование memory_usage для измерения памяти
    mem_usage = memory_usage((savitzky_golay_filter, (data,)), max_usage=True, retval=True) # менять функцию фильтра
    return mem_usage[1], mem_usage[0]



if __name__ == '__main__':
    data = pd.read_csv('positions_long.csv').to_numpy()
    tracking_visualization(data)
    
    # Сравнение затраченных ресурсов
    _, analysis_result = profile_function(data)
    _, max_memory_usage = profile_memory(data)
    print("Profiling Results:\n", analysis_result)
    print("Max Memory Usage:", max_memory_usage, "MiB")
    

    data = pd.read_csv('positions_short.csv').to_numpy()
    filtered_data1 = moving_average_filter(data)
    filtered_data2 = median_filter(data)
    filtered_data3 = kalman_filter(data)
    filtered_data4 = gaussian_filter(data)
    filtered_data5 = savitzky_golay_filter(data)

    # Визуальный анализ
    comparison_subplot(
        data[:,1][50:125], 
        [
            filtered_data1[:,1][50:125], 
            filtered_data2[:,1][50:125], 
            filtered_data3[:,1][50:125], 
            filtered_data4[:,1][50:125], 
            filtered_data5[:,1][50:125]
        ],
        ['Скользящее среднее', 'Медианный фильтр', 'Фильтр Калмана', 'Фильтр Гаусса', 'Фильтр Савицкого-Голея'],
        'Z'
    )

    # Изменение дисперсии
    def calculate_variance_reduction(original_data, filtered_data):
        original_variance = np.var(original_data, axis=0)
        filtered_variance = np.var(filtered_data, axis=0)
        variance_reduction = 100 * (original_variance - filtered_variance) / original_variance
        return variance_reduction

    variance_reduction = calculate_variance_reduction(data, filtered_data1)
    print(f"Уменьшение дисперсии (Скользящее среднее): {variance_reduction}%")

    variance_reduction = calculate_variance_reduction(data, filtered_data2)
    print(f"Уменьшение дисперсии (Медианный фильтр): {variance_reduction}%")

    variance_reduction = calculate_variance_reduction(data, filtered_data3)
    print(f"Уменьшение дисперсии (Фильтр Калмана): {variance_reduction}%")

    variance_reduction = calculate_variance_reduction(data, filtered_data4)
    print(f"Уменьшение дисперсии (Фильтр Гаусса): {variance_reduction}%")

    variance_reduction = calculate_variance_reduction(data, filtered_data5)
    print(f"Уменьшение дисперсии (Фильтр Савицкого-Голея): {variance_reduction}%")
    
    # Анализ краевых эффектов
    def edge_effect_analysis(original_data, filtered_data):
        start_diff = np.abs(original_data[0] - filtered_data[0])
        end_diff = np.abs(original_data[-1] - filtered_data[-1])
        
        return start_diff, end_diff

    start_diff, end_diff = edge_effect_analysis(data, filtered_data1)
    print("Скользящее среднее")
    print("Разница на начальном крае:", start_diff)
    print("Разница на конечном крае:", end_diff)

    start_diff, end_diff = edge_effect_analysis(data, filtered_data2)
    print("Медианный фильтр")
    print("Разница на начальном крае:", start_diff)
    print("Разница на конечном крае:", end_diff)

    start_diff, end_diff = edge_effect_analysis(data, filtered_data3)
    print("Фильтр Калмана")
    print("Разница на начальном крае:", start_diff)
    print("Разница на конечном крае:", end_diff)

    start_diff, end_diff = edge_effect_analysis(data, filtered_data4)
    print("Фильтр Гаусса")
    print("Разница на начальном крае:", start_diff)
    print("Разница на конечном крае:", end_diff)

    start_diff, end_diff = edge_effect_analysis(data, filtered_data5)
    print("Фильтр Савицкого-Голея")
    print("Разница на начальном крае:", start_diff)
    print("Разница на конечном крае:", end_diff)
    
    # Проверка на консистентность
    def consistency_check(original_data, filtered_data):
        # Рассчитываем разности между последовательными точками
        original_diff = np.diff(original_data, axis=0)
        filtered_diff = np.diff(filtered_data, axis=0)
        
        # Рассчитываем среднеквадратичное отклонение (СКО) разностей
        original_diff_std = np.std(original_diff, axis=0)
        filtered_diff_std = np.std(filtered_diff, axis=0)
        
        return original_diff_std, filtered_diff_std


    original_diff_std, filtered_diff_std = consistency_check(data, filtered_data1)
    print("СКО разностей исходных данных:", original_diff_std)
    print("СКО разностей фильтрованных данных:", filtered_diff_std)

    _, filtered_diff_std = consistency_check(data, filtered_data2)
    print("СКО разностей фильтрованных данных:", filtered_diff_std)

    _, filtered_diff_std = consistency_check(data, filtered_data3)
    print("СКО разностей фильтрованных данных:", filtered_diff_std)

    _, filtered_diff_std = consistency_check(data, filtered_data4)
    print("СКО разностей фильтрованных данных:", filtered_diff_std)

    _, filtered_diff_std = consistency_check(data, filtered_data5)
    print("СКО разностей фильтрованных данных:", filtered_diff_std)
