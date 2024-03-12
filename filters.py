import numpy as np
from scipy.signal import medfilt
from pykalman import KalmanFilter
from scipy.ndimage import gaussian_filter1d
from scipy.signal import savgol_filter




# Фильтрация шума: скользящее среднее
def moving_average_filter(data, window_size=5):
    filtered_data = np.convolve(data[:, 0], np.ones(window_size)/window_size, mode='valid')
    filtered_data = np.column_stack((filtered_data, np.convolve(data[:, 1], np.ones(window_size)/window_size, mode='valid')))
    filtered_data = np.column_stack((filtered_data, np.convolve(data[:, 2], np.ones(window_size)/window_size, mode='valid')))
    return filtered_data

# Фильтрация шума: медианный фильтр
def median_filter(data, kernel_size=5):
    filtered_data_x = medfilt(data[:, 0], kernel_size=kernel_size)
    filtered_data_y = medfilt(data[:, 1], kernel_size=kernel_size)
    filtered_data_z = medfilt(data[:, 2], kernel_size=kernel_size)
    return np.stack((filtered_data_x, filtered_data_y, filtered_data_z), axis=1)

# Фильтрация шума: фильтр Калмана
def kalman_filter(data):
    initial_state = data[0]
    observation_covariance = np.eye(3) * 0.1 
    transition_covariance = np.eye(3) * 0.1  
    transition = np.eye(3)

    kf = KalmanFilter(initial_state_mean=initial_state,
                      initial_state_covariance=observation_covariance,
                      observation_covariance=observation_covariance,
                      transition_covariance=transition_covariance,
                      transition_matrices=transition)

    kalman_smoothed, _ = kf.smooth(data)
    return kalman_smoothed


# Фильтрация шума: фильтр Гаусса
def gaussian_filter(data, sigma=1.5):
    filtered_data_x = gaussian_filter1d(data[:, 0], sigma=sigma)
    filtered_data_y = gaussian_filter1d(data[:, 1], sigma=sigma)
    filtered_data_z = gaussian_filter1d(data[:, 2], sigma=sigma)
    return np.stack((filtered_data_x, filtered_data_y, filtered_data_z), axis=1)


# Фильтрация шума: фильтр Савицкого-Голея
def savitzky_golay_filter(data, window_length=5, polyorder=2):
    if window_length % 2 == 0:  # Убедимся, что размер окна нечетный
        window_length += 1

    # Проверяем, что window_length больше polyorder
    if window_length <= polyorder:
        raise ValueError("window_length должен быть больше polyorder")

    filtered_data_x = savgol_filter(data[:, 0], window_length=window_length, polyorder=polyorder, mode='nearest')
    filtered_data_y = savgol_filter(data[:, 1], window_length=window_length, polyorder=polyorder, mode='nearest')
    filtered_data_z = savgol_filter(data[:, 2], window_length=window_length, polyorder=polyorder, mode='nearest')
    return np.stack((filtered_data_x, filtered_data_y, filtered_data_z), axis=1)