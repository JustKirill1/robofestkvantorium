import cv2


# Обработчик (пустой) событий трэкбара
def nothing(a):
    pass


# Создаем окно для элементов управления
cv2.namedWindow('Tracking')
cv2.createTrackbar('ThL', 'Tracking', 0, 255, nothing)
cv2.createTrackbar('ThH', 'Tracking', 255, 255, nothing)

# Подключаемся к камере
cap = cv2.VideoCapture(1)

# Запускаем бесконечный цикл
while True:
    # Получаем изображение с камеры
    _, frame = cap.read()
    # Уменьшаем (масштабируем) изображение
    scale = 0.6
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    frame = cv2.resize(frame, (width, height), interpolation=cv2.INTER_AREA)
    # Выводим изображение на экран
    cv2.imshow('Video', frame)
    # Переводим изобрадение в градации серого
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Выводим изображение на экран
    cv2.imshow('Gray', gray)
    # Получаем значения трэкбаров
    th_l = cv2.getTrackbarPos('ThL', 'Tracking')
    th_h = cv2.getTrackbarPos('ThH', 'Tracking')
    # Бинаризуем изображение
    _, th = cv2.threshold(gray, th_l, th_h, cv2.CHAIN_APPROX_NONE)
    # Выводим изображение на экран
    cv2.imshow('Binary', th)
    # Проверяем, не нажата ли кнопка q
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Освобождаем камеру
cap.release()
# Закрываем все окна
cv2.destroyAllWindows()
