import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton,
QLabel, QVBoxLayout, QHBoxLayout, QGridLayout, QLCDNumber,
                             QFrame)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QCoreApplication, QSize, Qt

from webCam import *

# from feature import main_traffic

class TrafficLight(QWidget):

    def __init__(self):
        super().__init__()
        size = QSize(1700, 1000)
        self.initUI(size)
        self.video = video(self, QSize(self.frm.width(), self.frm.height()))

    def initUI(self, size):
        # 신호등 빨간불 이미지
        red = QPixmap('image/redOff.jpeg')
        red_img = QLabel()
        red_img.setPixmap(red)
        rbox = QVBoxLayout()
        rbox.addWidget(red_img)

        # 신호등 파란불 이미지
        green = QPixmap('image/greenOff.jpeg')
        green_img = QLabel()
        green_img.setPixmap(green)
        gbox = QVBoxLayout()
        gbox.addWidget(green_img)

        # 신호등 파란불 남은 시간
        lcd = QLCDNumber(self)
        # lcd.display(time.sec)
        lcd.setStyleSheet('color: green')
        lcd.setFixedSize(200, 200)

        # 신호등 레이아웃
        lightLayout = QGridLayout()
        lightLayout.setSpacing(0)
        lightLayout.addLayout(rbox, 0, 0)
        lightLayout.addLayout(gbox, 1, 0)
        lightLayout.addWidget(lcd, 2, 0)

        # 시작 버튼
        self.sbtn = QPushButton('Start', self)
        self.sbtn.setStyleSheet('background-color: grey; color: white')
        self.sbtn.clicked.connect(self.onoffCam)

        # 종료 버튼
        self.qbtn = QPushButton('Quit', self)
        self.qbtn.setStyleSheet('background-color: grey; color: white')
        self.qbtn.clicked.connect(self.qbtn_clicked)

        # 버튼 레이아웃
        btnBox = QHBoxLayout()
        btnBox.addWidget(self.sbtn)
        btnBox.addWidget(self.qbtn)

        # 현재 상태 표시 문구
        stateStr = '프로그램 시작 전입니다.'
        state = QLabel(stateStr)
        state.setAlignment(Qt.AlignCenter)

        # 현재 상태, 버튼 레이아웃
        runLayout = QVBoxLayout()
        runLayout.addWidget(state)
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

    def onoffCam(self, e):
        self.video.startCam()

    # def sbtn_clicked(self):
    #    main_traffic()


    def qbtn_clicked(self):
        QCoreApplication.instance.quit()
        click = "close"


    def recvImage(self, img):
        self.frm.setPixmap(QPixmap.fromImage(img))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TrafficLight()
    sys.exit(app.exec_())
