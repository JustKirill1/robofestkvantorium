import threading
import time
import cv2
import numpy as np
c = threading.Condition()
cap = cv2.VideoCapture(0)
color = []
first = 0
second = 0
third = 0
a = 1
b = 0
class SUKA(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        global a
        global b
        global cap
        global color
        global first
        global second
        global third
        while True:
            c.acquire()
            if a == 1:
                while (1):

                    _, frame = cap.read()

                    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

                    red2 = cv2.inRange(hsv, (170, 50, 130), (180, 255, 255))
                    blue = cv2.inRange(hsv, (95, 50, 50), (120, 255, 255))
                    green = cv2.inRange(hsv, (40, 40, 40), (70, 255, 255))

                    b_mean = np.mean(blue)
                    g_mean = np.mean(green)
                    r_mean = np.mean(red2)

                    if (b_mean > g_mean and b_mean > r_mean):
                        if 'b' not in color:
                            color += 'b'
                            print(color)

                    if (g_mean > r_mean and g_mean > b_mean):
                        if 'g' not in color:
                            color += 'g'
                            print(color)

                    if (r_mean > g_mean and r_mean > b_mean):
                        if 'r' not in color:
                            color += 'r'
                            print(color)

                    res = cv2.bitwise_and(frame, frame, mask=red2)
                    res1 = cv2.bitwise_and(frame, frame, mask=blue)
                    res2 = cv2.bitwise_and(frame, frame, mask=green)
                    cv2.imshow('frame', frame)
                    cv2.imshow('red', res)
                    cv2.imshow('blue', res1)
                    cv2.imshow('green', res2)
                    k = cv2.waitKey(5) & 0xFF
                    if len(color) == 3 and a == 1:
                        time.sleep(3)
                        a += 1
                c.notify_all()
            else:
                c.wait()
            c.release()


class Ebanaya(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        global a
        global b
        global b_mean
        global g_mean
        global r_mean
        while True:
            c.acquire()
            if a == 2:
                if b_mean > g_mean and b_mean > r_mean and color.index('b') == 0 and first == 0:
                    first += 1
                    print("It's first blue ship")
                if g_mean > r_mean and g_mean > b_mean and color.index('g') == 0 and first == 0:
                    first += 1
                    print("It's first green ship")
                if r_mean > g_mean and r_mean > b_mean and color.index('r') == 0 and first == 0:
                    first += 1
                    print("It's first red ship")
                if b_mean > g_mean and b_mean > r_mean and color.index('b') == 1 and second == 0:
                    second += 1
                    print("It's second blue ship")
                if g_mean > r_mean and g_mean > b_mean and color.index('g') == 1 and second == 0:
                    second += 1
                    print("It's second green ship")
                if r_mean > g_mean and r_mean > b_mean and color.index('r') == 1 and second == 0:
                    second += 1
                    print("It's second red ship")
                if b_mean > g_mean and b_mean > r_mean and color.index('b') == 2 and third == 0:
                    third += 1
                    print("It's third blue ship")
                if g_mean > r_mean and g_mean > b_mean and color.index('g') == 2 and third == 0:
                    third += 1
                    print("It's third green ship")
                if r_mean > g_mean and r_mean > b_mean and color.index('r') == 2 and third == 0:
                    third += 1
                    print("It's third red ship")
                if first == 1 and second == 1 and third == 1:
                    a = 3
                    print("Все заебись!")
            else:
                c.wait()
            c.release()
x = SUKA("myThread_name_A")
z = Ebanaya("myThread_name_B")

x.start()
z.start()

x.join()
z.join()
