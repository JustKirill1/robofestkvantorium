import cv2
import numpy as np
import math
import time

cap = cv2.VideoCapture(1)
color = []
first = 0
second = 0
third = 0
zadershka = 0
while (1):

    _, frame = cap.read()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    red1 = cv2.inRange(hsv, (0, 50, 20), (5, 255, 255))
    red2 = cv2.inRange(hsv, (170, 50, 130), (180, 255, 255))
    blue = cv2.inRange(hsv, (87, 156, 50), (120, 255, 255))
    green = cv2.inRange(hsv, (40, 80, 40), (80, 255, 255))
    red = cv2.bitwise_or(red1, red2)
    b_mean = np.mean(blue)
    g_mean = np.mean(green)
    r_mean = np.mean(red)
    res = cv2.bitwise_and(frame, frame, mask=red)
    res1 = cv2.bitwise_and(frame, frame, mask=blue)
    res2 = cv2.bitwise_and(frame, frame, mask=green)
    b_perc = (np.sum(res1) / np.size(res1))/255*100
    g_perc = (np.sum(res2) / np.size(res2))/255*100
    r_perc = (np.sum(res)/np.size(res))/255*100
    #print("процент содержания синего %.2f " % b_perc)
    #print("процент содержания зеленного %.2f " % g_perc)
    #print("процент содержания красного %.2f " % r_perc)

    if b_mean > g_mean and b_mean > r_mean and b_perc > 1.5:
        if 'b' not in color:
            color += 'b'
            print(color)

    if g_mean > r_mean and g_mean > b_mean and g_perc > 1.5:
        if 'g' not in color:
            color += 'g'
            print(color)

    if r_mean > g_mean and r_mean > b_mean and r_perc > 1.5:
        if 'r' not in color:
            color += 'r'
            print(color)



    cv2.imshow('frame', frame)
    cv2.imshow('red', res)
    cv2.imshow('blue', res1)
    cv2.imshow('green', res2)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break