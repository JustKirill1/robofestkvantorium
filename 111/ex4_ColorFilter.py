import cv2
import numpy as np


# Обработчик (пустой) событий трэкбара
def nothing(a):
    pass


# Создаем окно для элементов управления
cv2.namedWindow('Tracking')
cv2.createTrackbar('LH', 'Tracking', 0, 255, nothing)
cv2.createTrackbar('LS', 'Tracking', 0, 255, nothing)
cv2.createTrackbar('LV', 'Tracking', 0, 255, nothing)
cv2.createTrackbar('HH', 'Tracking', 255, 255, nothing)
cv2.createTrackbar('HS', 'Tracking', 255, 255, nothing)
cv2.createTrackbar('HV', 'Tracking', 255, 255, nothing)

# Подключаемся к камере
cap = cv2.VideoCapture(1)

# Запускаем бесконечный цикл
while True:
    # Получаем изображение с камеры
    _, frame = cap.read()
    # Избавляемся от шумов (замыливаем)
    frame = cv2.blur(frame, (5, 5))
    # Уменьшаем (масштабируем) изображение
    scale = 0.6
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    frame = cv2.resize(frame, (width, height), interpolation=cv2.INTER_AREA)
    # Выводим изображение на экран
    cv2.imshow('Video', frame)
    # Создаем границы фильтра
    l_hsv = np.array([
        cv2.getTrackbarPos('LH', 'Tracking'),
        cv2.getTrackbarPos('LS', 'Tracking'),
        cv2.getTrackbarPos('LV', 'Tracking')
    ])
    h_hsv = np.array([
        cv2.getTrackbarPos('HH', 'Tracking'),
        cv2.getTrackbarPos('HS', 'Tracking'),
        cv2.getTrackbarPos('HV', 'Tracking')
    ])
    # Преобразуем изображение в HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # Применяем фильтр
    mask = cv2.inRange(hsv, l_hsv, h_hsv)
    # Выводим маску на экран
    cv2.imshow('Mask', mask)
    # Суммируем исходное изображение и маску
    masked = cv2.bitwise_and(frame, frame, mask=mask)
    # Выводим результат на экран
    cv2.imshow('Masked', masked)
    # Проверяем, не нажата ли кнопка q
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print(l_hsv, h_hsv)
        break

# Освобождаем камеру
cap.release()
# Закрываем все окна
cv2.destroyAllWindows()
