import cv2 as cv
import numpy as np
import serial
def circleDetection():
    img = cv.VideoCapture(1)
    img = cv.resize(img, (500, 400))
    output = img.copy()
    while (True):
        gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        blur = cv.medianBlur(gray_img, 5)
        circles = cv.HoughCircles(blur, cv.HOUGH_GRADIENT,
                                  1, 100, 10, param1=130, param2=55, minRadius=5, maxRadius=0)

        detected_circles = np.uint16(np.around(circles))

        for (x, y, r) in detected_circles[0, :]:
            cv.circle(output, (x, y), r, (0, 255, 0), 3)
            cv.circle(output, (x, y), 2, (255, 0, 0), 3)

        cv.imshow("Original Image", img)
        cv.imshow("Output", output)
        if cv.waitKey(1) == 27:  # esc Key
            break
    img.release()
    cv.destroyAllWindows()