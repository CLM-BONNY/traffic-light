import cv2
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from threading import Thread
import time


class video(QObject):
    sendImage = pyqtSignal(QImage)

    def __init__(self, widget, size):
        super().__init__()
        self.widget = widget
        self.size = size
        self.sendImage.connect(self.widget.recvImage)

        self.detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.color = [QColor(255, 0, 0), QColor(255, 128, 0), QColor(255, 255, 0), QColor(0, 255, 0), QColor(0, 0, 255),
                      QColor(0, 0, 128), QColor(128, 0, 128)]

    def startCam(self):
        try:
            self.cap = cv2.VideoCapture(0)
        except Exception as e:
            print('Cam Error : ', e)
        else:
            self.bThread = True
            self.thread = Thread(target=self.threadFunc)
            self.thread.start()

    def threadFunc(self):
        while self.bThread:
            ok, frame = self.cap.read()
            if ok:
                # detect image
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = self.detector.detectMultiScale(gray, 1.3, 5)

                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb.shape
                bytesPerLine = ch * w
                img = QImage(rgb.data, w, h, bytesPerLine, QImage.Format_RGB888)
                resizedImg = img.scaled(self.size.width(), self.size.height())
                self.sendImage.emit(resizedImg)
            else:
                print('cam read errror')

            time.sleep(0.01)

        print('thread finished')