<h1 align="center">Установка окружения</h1>


<h2 align="center">Установка <code>Intel RealSense SDK 2.0 (v2.50.0)</code></h2>

Так как, мы использум камеру Intel RealSense T265, нам необходимо ставить SDK с версией 2.50.0. Более поздние версии не будут работать с этой моделью камеры.

1. Установим необходимые зависимости:

```bash
sudo apt-get update
sudo apt-get install git libssl-dev libusb-1.0-0-dev pkg-config libgtk-3-dev
sudo apt-get install libglfw3-dev libgl1-mesa-dev libglu1-mesa-dev
```

2. Склонируем репозиторий с `RealSense SDK 2.0`:

```bash
git clone https://github.com/IntelRealSense/librealsense.git
cd librealsense
```

3. Переключимся на тэг с необходимой нам версией (v2.50.0):

```bash
git checkout v2.50.0
```

4. Установим `Cmake` и `компилятор C++`:

```bash
sudo apt-get install cmake
```

```bash
sudo apt-get install build-essential
```

5. Соберём проект с помощью `Cmake`:

```bash
mkdir build && cd build
cmake ../ -DCMAKE_BUILD_TYPE=Release
make -j$(nproc)
sudo make install
```

6. Добавим правила `udev` для нашей камеры:
* Заходим в папку конфигурации нашего проекта:
```bash
cd librealsense/config
```
* Скопируем правила `udev` в системную директорию:
```bash
sudo cp 99-realsense-libusb.rules /etc/udev/rules.d/
```
* Перезагрузим правила `udev`, чтобы система начала их использовать:
```bash
sudo udevadm control --reload-rules && sudo udevadm trigger
```

7. Проверим, что всё работает с помощью команды `realsense-viewer`. Если в запусившимся окне появилась наша камера, значит всё прошло успешно. 

---

<h2 align="center">Установка библиотеки <code>pyrealsense2</code></h2>

1. Для начала установим `python` и пакетный менеджер `pip`:

```bash
sudo apt update
sudo apt install python3
sudo apt install python3-pip
```

2. Проверим что установка прошла успешно:

```bash
python3 --version
pip3 --version
```

3. Установим библиотеку `pyrealsense2`:

```bash
pip install pyrealsense2
```

4. Проверим что библиотека успешно установлена (посмотрим список библиотек):

```bash
pip list
```

5. Напишем и запустим простейший скрипт для проверки работоспособности библиотеки:

* Создадим файл `script.py`
```python
import pyrealsense2 as rs
pipe = rs.pipeline()
profile = pipe.start()
try:
  for i in range(0, 100):
    frames = pipe.wait_for_frames()
    for f in frames:
      print(f.profile)
finally:
    pipe.stop()
```

* Запустим файл `script.py`
```bash
python script.py
```
---

<h2 align="center">Список источников</code></h2>

1. Установка Intel RealSense SDK 2.0 (v2.50.0) – https://github.com/IntelRealSense/librealsense/releases/tag/v2.50.0
2. Установка pyrealsense2 – https://pypi.org/project/pyrealsense2/
