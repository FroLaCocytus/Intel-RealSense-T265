import pyrealsense2 as rs
import time

# Создаем объект pipeline для управления потоками данных
pipeline = rs.pipeline()
config = rs.config()

# Настраиваем pipeline на использование камеры T265
config.enable_stream(rs.stream.pose)

# Начинаем получать потоки данных с камеры
pipeline.start(config)

try:
    while True:
        # Ожидаем новый набор кадров
        frames = pipeline.wait_for_frames()
        # Получаем кадр с данными о позиции
        pose_frame = frames.get_pose_frame()
        if pose_frame:
            # Получаем данные о позиции и ориентации
            data = pose_frame.get_pose_data()
            print("Позиция: x={:.2f}, y={:.2f}, z={:.2f}".format(data.translation.x, data.translation.y, data.translation.z))
            print("Ориентация: x={:.2f}, y={:.2f}, z={:.2f}, w={:.2f}".format(data.rotation.x, data.rotation.y, data.rotation.z, data.rotation.w))
            print()

        time.sleep(2)
except Exception as e:
    print(e)
finally:
    # Останавливаем поток данных
    pipeline.stop()
