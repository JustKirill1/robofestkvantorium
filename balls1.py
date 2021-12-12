import cv2
import numpy as np
import serial

cap = cv2.VideoCapture(1)
width = 320
height = 240
dim = (width, height)
while(True):
    _, frame = cap.read()
    gray = cv2.medianBlur(cv2.cvtColor(cap.read()[1], cv2.COLOR_BGR2GRAY),5)
    resized = cv2.resize(gray,dim,interpolation = cv2.INTER_AREA)
    circ = cv2.HoughCircles(resized,cv2.HOUGH_GRADIENT,1,50,param1=50,param2=35,
                              minRadius=0,maxRadius=0)
    cv2.imshow('video',resized)
    if circ is not None:
        circ = np.uint16(np.around(circ))[0,:]
        for j in circ:
            radius = cv2.circle(resized, (j[0], j[1]), j[2], (255, 255, 255), 2)
            center = cv2.circle(resized, (j[0], j[1]), 2, (255, 255, 255), 3)
        print(circ)
        cv2.imshow('original', frame)
        cv2.imshow('video',resized)
        if cv2.waitKey(1)==27:# esc Key
            break
cap.release()
cv2.destroyAllWindows()