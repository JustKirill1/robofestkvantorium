import threading
import time
с
c = threading.Condition()
a = 1
b = 0
class SUKA(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        global a
        global b
        while True:
            c.acquire()
            if a == 1:
                b += 2
                print(b)
                time.sleep(1)
                a = 2
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
        while True:
            c.acquire()
            if a == 2:

                b += 1
                print(b)
                time.sleep(1)
                a = 1
                c.notify_all()
            else:
                c.wait()
            c.release()
x = SUKA("myThread_name_A")
z = Ebanaya("myThread_name_B")

x.start()
z.start()

x.join()
z.join()
