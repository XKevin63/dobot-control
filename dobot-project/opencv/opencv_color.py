from cmath import acos
import sys
import time
import cv2
import numpy as np
import glob




def eye_in_hand(w=3, h=3):
    dobot_coordinate = np.array([[[286,18]],
                                 [[286,-7]],
                                 [[286,-33]],
                                 [[261,18]],
                                 [[261,-7]],
                                 [[261,-33]],
                                 [[236,18]],
                                 [[236,-7]],
                                 [[236,33]]])

    img = cv2.imread('/home/kevin/project/dobot-project/opencv/background.jpg', 1)
    img = cv2.resize(img, (1000,800))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # cv2.imshow('img_gray', gray)

    ret, corners = cv2.findChessboardCorners(gray, (w, h), None)
    # print(corners)
    if ret != True:
        print("error!!!!!!!!!!")
        sys.exit()

    cv2.drawChessboardCorners(img, (w,h), corners, ret)
    # cv2.imshow('img_corners', img)
    # cv2.waitKey(0)

    M = cv2.estimateAffine2D(corners, dobot_coordinate)

    return M[0]





def color_location(color_type, pic_path, show_key=0):
    # color threshold
    lower_blue = np.array([110,90,90])
    upper_blue = np.array([140,255,255])
    lower_yellow = np.array([22,90,90])
    upper_yellow = np.array([38,255,255])
    lower_green = np.array([38,90,90])
    upper_green = np.array([75,255,255])
    lower_red = np.array([150,15,15])
    upper_red = np.array([175,45,45])
    
    lower = eval('lower_' + color_type)
    upper = eval('upper_' + color_type)

    img = cv2.imread(pic_path, 1)
    img = cv2.resize(img, (1000,800))
    # cv2.imshow('orign_img', img)
    img_HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # cv2.imshow('HSV_img', img_HSV)

    mask = cv2.inRange(img_HSV, lower, upper)
    res = cv2.bitwise_and(img, img, mask=mask)

    # cv2.imshow('blue', res)

    gaus_img = cv2.GaussianBlur(res,(5,5),1.5)
    # cv2.imshow('gaus', gaus_img)

    gray_img = cv2.cvtColor(gaus_img,cv2.COLOR_BGR2GRAY)
    # cv2.imshow('gary', gray_img)

    ret, binary = cv2.threshold(gray_img,10,255,cv2.THRESH_BINARY | cv2.THRESH_TRIANGLE)
    # print("threshold value %s"%ret)
    # cv2.imshow('threshold',binary)

    # open calculate 2 times, didn't use!!!!!!!!
    kernel = np.ones((5,5),np.uint8)
    opening = cv2.morphologyEx(binary,cv2.MORPH_OPEN,kernel, iterations=3) 
    # cv2.imshow('open',opening)

    # Draw outline
    contours, hierarchy = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(img,contours,-1,(255,0,255),2)
    # cv2.imshow('contours', img)  
    # Calculate center point coordinates
    coordinates_list = []
    a_list = []
    for i in range(len(contours)):
        ep = 0.02*cv2.arcLength(contours[i], True)
        ap = cv2.approxPolyDP(contours[i], ep, True)
        for p in ap:
            img = cv2.circle(img, (p[0][0],p[0][1]), 3, (0,255,0), -1)
            img = cv2.circle(img, (0,50), 3, (0,0,255) ,-1)
        x = ap[1][0][0] - ap[0][0][0]
        y = ap[1][0][1] - ap[0][0][1]
        cosa = y/((x**2 + y**2)**0.5)
        a = acos(cosa)
        a_list.append(a.real)

        M = cv2.moments(contours[i])
        # print(M["m00"])
        print("the",i+1, "S:", M["m00"])
        center_x = int(M["m10"] / M["m00"])
        center_y = int(M["m01"] / M["m00"])
        w = []
        w.append(center_x)
        w.append(center_y)
        w.append(M["m00"])
        coordinates_list.append(w)
        m_image = cv2.circle(img, (center_x, center_y), 3, (255,0,255), -1)  # 绘制中心点

    if show_key == 1:
        cv2.imshow('circle', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    print('we have', len(coordinates_list), color_type, 'location to work')
    for i in range(len(coordinates_list)):
        print('the', i+1, 'location is:', coordinates_list[i])



    return coordinates_list, a_list




def vedio(device_number):
    device = cv2.VideoCapture(device_number)

    if device.isOpened():
        ret, frame = device.read()
        cv2.imwrite('/home/kevin/project/dobot-project/picture_work/capture.jpg', frame)
        device.release()
    
    else:
        print('check your device connect!!!!!')

    return device
    
    




# x,y = color_location(color_type='yellow', pic_path='/home/kevin/project/dobot-project/opencv/MVS-picture.jpg')
# print(x,y)