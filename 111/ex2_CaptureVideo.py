import cv2

# Подключаемся к камере
cap = cv2.VideoCapture(1)

# Запускаем бесконечный цикл
while True:
    # Получаем изображение с камеры
    _, frame = cap.read()
    # Выводим изображение на экран
    cv2.imshow('Video', frame)
    # Проверяем, не нажата ли кнопка q
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Освобождаем камеру
cap.release()
# Закрываем все окна
cv2.destroyAllWindows()
