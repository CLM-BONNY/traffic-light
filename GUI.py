import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton,
QLabel, QVBoxLayout, QHBoxLayout, QGridLayout, QLCDNumber, QGroupBox)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QCoreApplication, Qt


class TrafficLight(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 신호등 빨간불 이미지
        red = QPixmap('image/red.png')
        red_img = QLabel()
        red_img.setPixmap(red)
        rbox = QVBoxLayout()
        rbox.addWidget(red_img)

        # 신호등 파란불 이미지
        green = QPixmap('image/green.png')
        green_img = QLabel()
        green_img.setPixmap(green)
        gbox = QVBoxLayout()
        gbox.addWidget(green_img)

        # 신호등 파란불 남은 시간
        lcd = QLCDNumber(self)
        lcd.setStyleSheet('color: green')
        lcd.setFixedSize(200, 200)

        # 신호등 레이아웃
        lightLayout = QGridLayout()
        lightLayout.setSpacing(0)
        lightLayout.addLayout(rbox, 0, 0)
        lightLayout.addLayout(gbox, 1, 0)
        lightLayout.addWidget(lcd, 2, 0)

        # 시작 버튼
        sbtn = QPushButton('Start', self)
        sbtn.setStyleSheet('background-color: grey; color: white')

        # 종료 버튼
        qbtn = QPushButton('Quit', self)
        qbtn.setStyleSheet('background-color: grey; color: white')
        qbtn.clicked.connect(QCoreApplication.instance().quit)

        # 버튼 레이아웃
        btnBox = QHBoxLayout()
        btnBox.addWidget(sbtn)
        btnBox.addWidget(qbtn)

        # 현재 상태 표시 문구
        state = QLabel('프로그램 시작 전입니다.')
        state.setAlignment(Qt.AlignCenter)

        # 현재 상태, 버튼 레이아웃
        runLayout = QVBoxLayout()
        runLayout.addWidget(state)
        runLayout.addLayout(btnBox)

        # 전체 레이아웃
        mainLayout = QGridLayout()
        mainLayout.setSpacing(30)
        mainLayout.addLayout(lightLayout, 0, 0)
        mainLayout.addLayout(runLayout, 1, 0)

        self.setLayout(mainLayout)
        self.setWindowTitle('TrafficLight')
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TrafficLight()
    sys.exit(app.exec_())