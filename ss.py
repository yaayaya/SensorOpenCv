import cv2 as cv
import math
import time , threading
import random
from datetime import datetime

import qwiic


print("VL53L1X Qwiic Test\n")
ToF = qwiic.QwiicVL53L1X()
if (ToF.sensor_init() == None): # Begin returns 0 on a good init
    print("Sensor online!\n")
distance = 0
def get_distance():
    global distance
    try:
        ToF.start_ranging() # Write configuration bytes to initiate measurement
        time.sleep(.03)
        distance = ToF.get_distance()# Get the result of the measurement from the sensor
        time.sleep(.03)
        ToF.stop_ranging()
        return distance
        # print("Distance(mm): %s" % (distance))
    except Exception as e:
        print(e)
        return distance

# 假資料取得
# _number = 2
# isPlus = True

# def getNumber():
#     global isPlus
#     global _number
#     if (isPlus and _number <= 100):
#         _number += 1
#         if (_number >= 100):
#             isPlus = False
#     elif (not isPlus and _number > 0):
#         _number -= 1
#         if (_number <= 2):
#             isPlus = True
#     return _number

# 設定模糊度  _d 距離(cm)
def getBlur(_d):
    _blur = 1
    if (_d  <= 20):
        _blur  = 100
    elif (_d  > 20 and _d  <= 40 ):
        _blur  = 100 - ((3/2)*(_d -20))
    elif(_d  > 40 and _d  <= 70)   :
        _blur  = 70 - ((5/3)*(_d -40))
    elif(_d  > 70 and _d  <= 100)  :
        _blur  = 20 - ((1/6)*(_d -70))
    elif(_d  > 100 and _d  <= 130) :
        _blur  = 15 - ((1/3)*(_d -100))
    elif(_d  > 130 and _d  <= 150) :
        _blur  = 5 - ((1/4)*(_d -130))
    else :
        _blur = 1
    return _blur

# 全螢幕使用
# cv.namedWindow("window", cv.WND_PROP_FULLSCREEN)
# cv.setWindowProperty("window",cv.WND_PROP_FULLSCREEN,cv.WINDOW_FULLSCREEN)

global startTime
startTime = datetime.now()
global nowImg
nowImg = 1
global isSubImg
isSubImg = False

while True :
    # 換主圖片
    timeDif = datetime.now() - startTime
    if (timeDif.seconds > 5):
        startTime = datetime.now()
        nowImg = 1 if nowImg == 4 else nowImg + 1

    # 模糊數據取得
    blurNum = getBlur(get_distance())

    # 非附圖片模式 模糊>70 開啟副圖片
    if (isSubImg == False):
        if blurNum > 70 :
            isSubImg = True
            subImg = random.randint(1,4)
            image = cv.imread(f'./static/img/s{subImg}.jpg', 1)
        else:
            image = cv.imread(f'./static/img/{nowImg}.jpg', 1)
    # 副圖片模式時 模糊小於70 回歸主圖片
    else:
        if (blurNum <= 70 ):
            isSubImg = False
            image = cv.imread(f'./static/img/{nowImg}.jpg', 1)

    print(blurNum)
    blurNum = math.floor(blurNum)
    # 模糊設置
    dst = cv.blur(image, (blurNum,blurNum))
    # 圖片刷新於window視窗上
    cv.imshow("window", dst)
    # 等候33毫秒
    cv.waitKey(33)

