import pyrealsense2 as rs
import time

class Tracker_Realsense_T265:
    def __init__(self, filepath):
        self.pipeline = rs.pipeline()
        self.config = rs.config()
        self.config.enable_stream(rs.stream.pose)
        self.filepath = filepath  # Путь к файлу для записи данных

    def start_tracking(self, duration_sec):
        # Запуск камеры
        self.pipeline.start(self.config)
        start_time = time.time()

        with open(self.filepath, 'w') as file: 
            file.write("x,y,z\n")  # Заголовок для столбцов с координатами
            try:
                while True:
                    # Проверка, не истекло ли заданное время
                    if time.time() - start_time > duration_sec:
                        break

                    frames = self.pipeline.wait_for_frames()
                    pose_frame = frames.get_pose_frame()
                    if pose_frame:
                        data = pose_frame.get_pose_data()
                        # Запись данных о позиции в файл
                        file.write(f"{data.translation.x},{data.translation.y},{data.translation.z}\n")
            finally:
                self.pipeline.stop()

    def stop(self):
        self.pipeline.stop()

tracker = Tracker_Realsense_T265(filepath="positions_short.csv")
tracking_duration = 16  # Задаем продолжительность трекинга в секундах
print("--------------------")
print("Начало сбора данных")
tracker.start_tracking(tracking_duration)
print("Сбор данных завершен и сохранен в файл")
print("--------------------")