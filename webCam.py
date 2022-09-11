import cv2
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from threading import Thread
import mediapipe as mp
import numpy as np


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
        global faces, status
        with self.mp_hands.Hands(
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5) as hands:
            while self.bThread:
                ok, frame = self.cap.read()
                if ok:
                    # 얼굴 인식
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    self.faces = self.detector.detectMultiScale(gray, 1.3, 5)

                    for (x, y, w, h) in self.faces:
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

                    # 손 인식
                    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                    image.flags.writeable = False
                    results = hands.process(image)

                    image.flags.writeable = True
                    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                    image_height, image_width, _ = image.shape

                    if results.multi_hand_landmarks:
                        for hand_landmarks in results.multi_hand_landmarks:

                            # 엄지를 제외한 나머지 4개 손가락의 마디 위치 관계를 확인하여 플래그 변수를 설정합니다. 손가락을 일자로 편 상태인지 확인합니다.
                            thumb_finger_state = 0
                            if hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_CMC].y * image_height > \
                                    hand_landmarks.landmark[
                                        self.mp_hands.HandLandmark.THUMB_MCP].y * image_height:
                                if hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_MCP].y * image_height > \
                                        hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_IP].y * image_height:
                                    if hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_IP].y * image_height > \
                                            hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP].y * image_height:
                                        thumb_finger_state = 1

                            index_finger_state = 0
                            if hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_MCP].y * image_height > \
                                    hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_PIP].y * image_height:
                                if hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_PIP].y * image_height > \
                                        hand_landmarks.landmark[
                                            self.mp_hands.HandLandmark.INDEX_FINGER_DIP].y * image_height:
                                    if hand_landmarks.landmark[
                                        self.mp_hands.HandLandmark.INDEX_FINGER_DIP].y * image_height > \
                                            hand_landmarks.landmark[
                                                self.mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_height:
                                        index_finger_state = 1

                            middle_finger_state = 0
                            if hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y * image_height > \
                                    hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y * image_height:
                                if hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y * image_height > \
                                        hand_landmarks.landmark[
                                            self.mp_hands.HandLandmark.MIDDLE_FINGER_DIP].y * image_height:
                                    if hand_landmarks.landmark[
                                        self.mp_hands.HandLandmark.MIDDLE_FINGER_DIP].y * image_height > \
                                            hand_landmarks.landmark[
                                                self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y * image_height:
                                        middle_finger_state = 1

                            ring_finger_state = 0
                            if hand_landmarks.landmark[self.mp_hands.HandLandmark.RING_FINGER_MCP].y * image_height > \
                                    hand_landmarks.landmark[self.mp_hands.HandLandmark.RING_FINGER_PIP].y * image_height:
                                if hand_landmarks.landmark[self.mp_hands.HandLandmark.RING_FINGER_PIP].y * image_height > \
                                        hand_landmarks.landmark[self.mp_hands.HandLandmark.RING_FINGER_DIP].y * image_height:
                                    if hand_landmarks.landmark[self.mp_hands.HandLandmark.RING_FINGER_DIP].y * image_height > \
                                            hand_landmarks.landmark[
                                                self.mp_hands.HandLandmark.RING_FINGER_TIP].y * image_height:
                                        ring_finger_state = 1

                            pinky_finger_state = 0
                            if hand_landmarks.landmark[self.mp_hands.HandLandmark.PINKY_MCP].y * image_height > \
                                    hand_landmarks.landmark[
                                        self.mp_hands.HandLandmark.PINKY_PIP].y * image_height:
                                if hand_landmarks.landmark[self.mp_hands.HandLandmark.PINKY_PIP].y * image_height > \
                                        hand_landmarks.landmark[self.mp_hands.HandLandmark.PINKY_DIP].y * image_height:
                                    if hand_landmarks.landmark[self.mp_hands.HandLandmark.PINKY_DIP].y * image_height > \
                                            hand_landmarks.landmark[self.mp_hands.HandLandmark.PINKY_TIP].y * image_height:
                                        pinky_finger_state = 1

                            if thumb_finger_state == 1 and index_finger_state == 1 and middle_finger_state == 1 and ring_finger_state == 1 and pinky_finger_state == 1:
                                self.status = "보"
                            elif thumb_finger_state == 1 and index_finger_state == 1 and middle_finger_state == 0 and ring_finger_state == 0 and pinky_finger_state == 0:
                                self.status = "가위"
                            elif index_finger_state == 0 and middle_finger_state == 0 and ring_finger_state == 0 and pinky_finger_state == 0:
                                self.status = "주먹"

                            image = np.array(image)

                            # 손가락 뼈대를 그려줍니다.
                            self.mp_drawing.draw_landmarks(
                                frame,
                                hand_landmarks,
                                self.mp_hands.HAND_CONNECTIONS,
                                self.mp_drawing_styles.get_default_hand_landmarks_style(),
                                self.mp_drawing_styles.get_default_hand_connections_style())

                    # 영상 보내기
                    rgb = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
                    h, w, ch = rgb.shape
                    bytesPerLine = ch * w
                    img = QImage(rgb.data, w, h, bytesPerLine, QImage.Format_RGB888)
                    resizedImg = img.scaled(self.size.width(), self.size.height())
                    self.sendImage.emit(resizedImg)
                else:
                    print('cam read errror')