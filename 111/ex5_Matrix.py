import cv2
import numpy as np


# Обработчик (пустой) событий трэкбара
def nothing(a):
    pass


# Определение цвета
def get_color(sec):
    # blue
    l_hsv = np.array([83, 141, 0])
    h_hsv = np.array([127, 255, 255])
    mask = cv2.inRange(sec, l_hsv, h_hsv)
    sh = sec.shape[1::-1]
    res = cv2.countNonZero(mask)/(sh[0]*sh[1])
    if res > 0.5:
        return "BLUE"

    # yellow
    l_hsv = np.array([12, 73, 149])
    h_hsv = np.array([43, 255, 255])
    mask = cv2.inRange(sec, l_hsv, h_hsv)
    sh = sec.shape[1::-1]
    res = cv2.countNonZero(mask) / (sh[0] * sh[1])
    if res > 0.5:
        return "YELLOW"

    # green
    l_hsv = np.array([31, 121, 23])
    h_hsv = np.array([82, 255, 255])
    mask = cv2.inRange(sec, l_hsv, h_hsv)
    sh = sec.shape[1::-1]
    res = cv2.countNonZero(mask) / (sh[0] * sh[1])
    if res > 0.5:
        return "GREEN"

    # red
    l_hsv = np.array([0, 50, 50])
    h_hsv = np.array([10, 255, 255])
    mask1 = cv2.inRange(sec, l_hsv, h_hsv)
    l_hsv = np.array([170, 50, 50])
    h_hsv = np.array([180, 255, 255])
    mask2 = cv2.inRange(sec, l_hsv, h_hsv)
    mask = mask1 + mask2
    sh = sec.shape[1::-1]
    res = cv2.countNonZero(mask) / (sh[0] * sh[1])
    if res > 0.5:
        return "RED"

    return "N/A"


# Создаем окно для элементов управления
cv2.namedWindow('Tracking')
cv2.createTrackbar('ThL', 'Tracking', 160, 255, nothing)
cv2.createTrackbar('ThH', 'Tracking', 255, 255, nothing)

# Kernel для преобразования
kernel = np.ones((5, 5), 'uint8')

# Подключаемся к камере
cap = cv2.VideoCapture(1)

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
    # Переводим изобрадение в градации серого
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # cv2.imshow('Gray', gray)
    # Получаем значения трэкбаров
    th_l = cv2.getTrackbarPos('ThL', 'Tracking')
    th_h = cv2.getTrackbarPos('ThH', 'Tracking')
    # Бинаризуем изображение
    _, th = cv2.threshold(gray, th_l, th_h, cv2.CHAIN_APPROX_NONE)
    # cv2.imshow('Binary', th)
    # Расширяем границы
    th = cv2.dilate(th, kernel, iterations=2)
    cv2.imshow('Dilated', th)
    # Получаем контуры из бинарного изображения
    contours, hierarchy = cv2.findContours(th, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    # Создаем копию исходного изображения
    res = frame.copy()
    # Проходим в цикле по всем контурам
    for contour in contours:
        # Апроксимируем контур
        approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
        r = approx.ravel()
        # Фильтруем только квадраты и прямоугольники
        if len(approx) == 4:
            # Получаем границы контура
            x, y, w, h = cv2.boundingRect(approx)
            # Проверяем размер и соотношение сторон (нам нужен квадрат)
            if 70 < w < 200 and 70 < h < 200:
                aspectRatio = float(w) / h
                if 0.9 <= aspectRatio < 1.1:
                    # Создаем маску для того, чтобы откинуть лишнее
                    mask = np.zeros(res.shape[:2], dtype="uint8")
                    cv2.fillPoly(mask, pts=[contour], color=255)
                    # Суммируем маску и изображение
                    res = cv2.bitwise_and(res, res, mask=mask)
                    # cv2.drawContours(res, [contour], 0, (255, 0, 0), 5)
                    # Определяем угол наклона
                    angle = np.rad2deg(np.arctan2(r[3] - r[1], r[2] - r[0]))
                    if angle > 135:
                        angle = angle - 180
                    else:
                        angle = angle - 90
                    #print(w, h, aspectRatio, angle)
                    # Выводим результат
                    cv2.imshow('Shapes', res)
                    # Обрезаем лишнее
                    cropped = res[y:y + h, x:x + w]
                    cv2.imshow('Cropped', cropped)
                    # Поворачиваем изображение
                    rot_center = tuple(np.array(cropped.shape[1::-1]) / 2)
                    rot_mat = cv2.getRotationMatrix2D(rot_center, angle, 1.0)
                    rot = cv2.warpAffine(cropped, rot_mat, cropped.shape[1::-1], flags=cv2.INTER_LINEAR)
                    cv2.imshow('Rotated', rot)
                    # Обрезаем повернутое
                    cvt = cv2.cvtColor(rot, cv2.COLOR_BGR2GRAY)
                    x, y, w, h = cv2.boundingRect(cvt)
                    cropped = rot[y:y + h, x:x + w]
                    cv2.imshow('Cropped2', cropped)
                    # Преобразуем в HSV
                    hsv = cv2.cvtColor(cropped, cv2.COLOR_BGR2HSV)
                    # Определяем цвет каждого из 9 участков
                    sx = int(w / 3)
                    sy = int(h / 3)
                    cols = [['', '', ''], ['', '', ''], ['', '', '']]
                    for ix in range(3):
                        for iy in range(3):
                            py = iy * sy
                            px = ix * sx
                            section = hsv[py:py+sy, px:px+sx]
                            cols[ix][iy] = get_color(section)
                    # Выводим результат
                    print(cols)
                    break

    # Проверяем, не нажата ли кнопка q
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Освобождаем камеру
cap.release()
# Закрываем все окна
cv2.destroyAllWindows()
