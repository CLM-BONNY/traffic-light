import time

# from webCam import faces, status
from GUI import TrafficLight

def time_sub():
    global sec
    sec = 5
    while sec != 0:
        sec = sec - 1
        time.sleep(1)


def time_add():
    sec += 4
    stateStr = '4초 추가되었습니다. \n안전하게 건너가십시오.'


def t_light_on():
    redState = 'image/redOff.jpeg'
    greenState = 'image/greenOn.png'
    stateStr = '안전하게 건너가십시오.'
    time.sleep(sec)


def t_light_off():
    redState = 'image/redOn.png'
    greenState = 'image/greenOff.jpeg'
    stateStr = '잠시만 기다려주십시오.'


def main_traffic():
    while TrafficLight.qbtn_clicked.click != "close":
        t_light_off()
        if status == "rock":
            t_light_on()
            time_sub()
        else:
            time.sleep(10)
        while faces != False:
            time.sleep(10)
        t_light_on()
        time_sub()
        if status == "scissors":
            time_add()
