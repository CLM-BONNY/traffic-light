import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton,
                             QLabel, QVBoxLayout, QHBoxLayout,
                             QGridLayout, QLCDNumber,QFrame)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QCoreApplication, QSize, Qt

import time

from webCam import *

class TrafficLight(QWidget):

    def __init__(self):
        super().__init__()
        self.flag = None
        size = QSize(1300, 900)
        self.sec = 0
        self.click = "open"
        self.red = QPixmap('image/redOff.jpeg')
        self.green = QPixmap('image/greenOff.png')
        self.initUI(size)
        self.video = video(self, QSize(self.frm.width(), self.frm.height()))


    def initUI(self, size):

        # 신호등 빨간불 이미지
        self.red_img = QLabel()
        self.red = QPixmap('image/redOff.jpeg')
        self.red_img.setPixmap(self.red)
        rbox = QVBoxLayout()
        rbox.addWidget(self.red_img)

        # 신호등 파란불 이미지
        self.green_img = QLabel()
        self.green = QPixmap('image/greenOff.jpeg')
        self.green_img.setPixmap(self.green)
        gbox = QVBoxLayout()
        gbox.addWidget(self.green_img)

        # 신호등 파란불 남은 시간
        self.lcd = QLCDNumber(self)
        self.lcd.display(self.sec)
        self.lcd.setStyleSheet('color: green')
        self.lcd.setFixedSize(200, 200)

        # 신호등 레이아웃
        lightLayout = QGridLayout()
        lightLayout.setSpacing(0)
        lightLayout.addLayout(rbox, 0, 0)
        lightLayout.addLayout(gbox, 1, 0)
        lightLayout.addWidget(self.lcd, 2, 0)

        # 시작 버튼
        self.sbtn = QPushButton('Start', self)
        self.sbtn.setStyleSheet('background-color: grey; color: white')
        self.sbtn.clicked.connect(self.sbtn_clicked)

        # 종료 버튼
        self.qbtn = QPushButton('Quit', self)
        self.qbtn.setStyleSheet('background-color: grey; color: white')
        self.qbtn.clicked.connect(self.qbtn_clicked)

        # 버튼 레이아웃
        btnBox = QHBoxLayout()
        btnBox.addWidget(self.sbtn)
        btnBox.addWidget(self.qbtn)

        # 현재 상태 표시 문구
        self.state = QLabel('프로그램 시작 전입니다.')
        self.state.setAlignment(Qt.AlignCenter)

        # 현재 상태, 버튼 레이아웃
        runLayout = QVBoxLayout()
        runLayout.addWidget(self.state)
        runLayout.addLayout(btnBox)

        # 웹캠 레이아웃
        self.frm = QLabel()
        self.frm.setFrameShape(QFrame.Panel)

        # 메인 윈도우 왼쪽 레이아웃
        leftLayout = QGridLayout()
        leftLayout.setSpacing(30)
        leftLayout.addLayout(lightLayout, 0, 0)
        leftLayout.addLayout(runLayout, 1, 0)

        # 전체 레이아웃
        mainLayout = QGridLayout()
        mainLayout.addLayout(leftLayout, 0, 0)
        mainLayout.addWidget(self.frm, 0, 1)

        self.setFixedSize(size)
        self.setLayout(mainLayout)
        self.setWindowTitle('TrafficLight')
        self.show()

    def sbtn_clicked(self, e):
        self.video.startCam()
        main = Thread(target=self.main_traffic)
        main.start()

    def qbtn_clicked(self):
        self.click = "close"
        a = QCoreApplication.instance()
        a.quit()

    def recvImage(self, img):
        self.frm.setPixmap(QPixmap.fromImage(img))

    def time_sub(self):
        self.wait = 3
        self.sec = 5
        while True:
            if self.sec == 0:
                self.t_light_off()
                break
            else:
                self.sec = self.sec - 1
                print('초록불 남은 시간', self.sec)
                self.lcd.display(self.sec)
                time.sleep(1)

    # 추후 수정
    # def time_add(self):
    #     # self.wait = 3
    #     self.sec += 4
    #     # 추후 수정
    #     # self.red = QPixmap('image/redOff.jpeg')
    #     # self.red_img.setPixmap(self.red)
    #     # self.green = QPixmap('image/greenOn.png')
    #     # self.green_img.setPixmap(self.green)
    #     self.state.setText('4초 추가되었습니다. \n안전하게 건너가십시오.')
    #     print('초록불 남은 시간', self.sec)
    #     QApplication.processEvents()

    def t_light_on(self):
        self.flag = "on"
        self.red = QPixmap('image/redOff.jpeg')
        self.red_img.setPixmap(self.red)
        self.green = QPixmap('image/greenOn.png')
        self.green_img.setPixmap(self.green)
        self.state.setText('안전하게 건너가십시오.')
        QApplication.processEvents()
        self.time_sub()

    def t_light_off(self):
        self.flag = "off"
        # 추후 수정
        # self.red = QPixmap('image/redOn.jpeg')
        # self.red_img.setPixmap(self.red)
        # self.green = QPixmap('image/greenOff.png')
        # self.green_img.setPixmap(self.green)
        self.state.setText('잠시만 기다려주십시오.')
        QApplication.processEvents()

    def main_traffic(self):
        self.wait = 3
        while self.click != 'close':
            self.video.status = ""
            time.sleep(1)
            if self.video.status == "주먹" and self.sec == 0:
                print('주먹 감지')
                timer = Thread(target=self.t_light_on)
                timer.start()

            # 추후 수정
            # if self.flag == 'on':
            #     if self.video.status == "가위" and self.sec <= 2:
            #         print('가위 감지')
            #         self.time_add()
            if self.sec == 0:
                self.wait -= 1
                print('빨간불 남은시간 :', self.wait)
            if self.wait <= 0:
                self.wait = 3
                if len(self.video.faces) != 0:
                    print('사람 얼굴 인식')
                    self.t_light_on()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TrafficLight()
    sys.exit(app.exec_())
