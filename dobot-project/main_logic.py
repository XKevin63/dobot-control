import os
import sys
import pydobot
import time


from opencv.opencv_color import color_location
from pydobot import Dobot
from serial.tools import list_ports
from dobot.base_pydobot import *


t_color ={'blue':[261,140], 'red':[311,92], 'green':[211,140], 'yellow':[261,-130]}




def sorting_block(clo, device, M, dic_z, show_key=0):
    w = 0
    os.system('clear')
    # color_l = color_location(color_type=clo, pic_path='/home/kevin/project/dobot-project/picture_work/blue.jpg')
    while True:
        os.system('python3 /home/kevin/project/dobot-project/MVS/MVS_control_start.py')
        pixel_coordinates, a_list = color_location(color_type=clo, pic_path='/home/kevin/project/dobot-project/opencv/MVS-picture.jpg', show_key=show_key)
        # target_z = dic_z[clo]
        # w = dic_z[clo] + w
        if len(pixel_coordinates) != 0:   
            i = 0
            target_z = dic_z[clo] * 27 - 34 - 5
            dobot_list = cv_to_dobot(cv_list=pixel_coordinates[i], M=M)
            x = dobot_list[0]
            y = dobot_list[1]
            xz = int(pixel_coordinates[i][2])
            # print(xz)
            # time.sleep(3)
            if xz >= 14500 and xz < 16600:
                z = -30
            elif xz >= 17600 and xz <= 19000:
                z = -7
            else:
                z = -7
            r = a_list[i] * 55
            try:
                print(target_z)
                t_x = t_color[clo][0]
                t_y = t_color[clo][1]
                device.move_to(x,y,40,0,wait=True)
                device.move_to(x,y,z,0,wait=True)
                device.grip(enable=True)
                device.move_to(x,y,30,0,wait=True)
                device.move_to(x,y,30,r,wait=True)
                (x1,y1,z1,r1,j1,j2,j3,j4) = device.pose()
                device.move_to(t_x,t_y,40,r1,wait=True)
                device.move_to(t_x,t_y,target_z,r1,wait=True)
                device.grip(enable=False)
                device.move_to(t_x,t_y,40,r1,wait=True)
                device_home(device=device)
                print("complete!")
                if dic_z[clo] < 3:
                    dic_z[clo] = dic_z[clo] + 1

            except:
                print("error, move!")
                return dic_z
            

        else:
            print("can't find appoint color")
            break

    # input("enter any key to continue.........")
    return dic_z






def dubug_coordinate(device):
    print("please put one blue placement block to any position")
    input("press any key to continue......")
    os.system("clear")
    os.system('python3 /home/kevin/project/dobot-project/MVS/MVS_control_start.py')
    color_l = color_location(color_type='blue', pic_path='/home/kevin/project/dobot-project/opencv/MVS-picture.jpg')
    if len(color_l) >= 1:    
        cv1 = color_l
    else:
        print("can't find appoint color or too many placement blocks")
        return 0
    while True:
        os.system("clear")
        print("input [8888] to break")
        try:
            (x,y,z,r,j1,j2,j3,j4) = device.pose()
        except:
            print("connect dobot error!")
            return 0
        x_target = int(input("increment of x:"))
        if x_target == 8888:
            break
        else:
            x = x + x_target
            try:
                device.move_to(x,y,z,r,wait=False)
            except:
                print("error x!")
                x = x - x_target
        y_target = int(input("increment of y:"))
        if y_target == 8888:
            break
        else:
            y = y + y_target
            try:
                device.move_to(x,y,z,r,wait=False)
            except:
                print("error y!")
                y = y - y_target
        z_target = int(input("increment of z:"))
        if z_target == 8888:
            break
        else:
            z = z + z_target
            try:
                device.move_to(x,y,z,r,wait=False)
            except:
                print("error z!")
                z = z - z_target
    dobot1 = [x,y]
    print(device.pose())

    print("please put one blue placement block to another position")
    input("press any key to continue......")
    os.system("clear")
    os.system('python3 /home/kevin/project/dobot-project/MVS/MVS_control_start.py')
    color_l = color_location(color_type='blue', pic_path='/home/kevin/project/dobot-project/opencv/MVS-picture.jpg')
    if len(color_l) == 1:    
        cv2 = color_l
    else:
        print("can't find appoint color or too many placement blocks")
        return 0
    while True:
        os.system("clear")
        print("input [8888] to break")
        x_target = int(input("increment of x:"))
        if x_target == 8888:
            break
        else:
            x = x + x_target
            try:
                device.move_to(x,y,z,r,wait=False)
            except:
                print("error x!")
                x = x - x_target
        y_target = int(input("increment of y:"))
        if y_target == 8888:
            break
        else:
            y = y + y_target
            try:
                device.move_to(x,y,z,r,wait=False)
            except:
                print("error y!")
                y = y - y_target
        z_target = int(input("increment of z:"))
        if z_target == 8888:
            break
        else:
            z = z + z_target
            try:
                device.move_to(x,y,z,r,wait=False)
            except:
                print("error z!")
                z = z - z_target
    dobot2 = [x,y]

    os.system('clear')
    print(device.pose())
    print("cv1:",cv1)
    print("cv2:",cv2)
    print("dobot1:",dobot1)
    print("dobot2:",dobot2)
    

        
        
        
def debug_eye_to_hand(device, M):
    pixel_coordinates, a_list = color_location(color_type='blue', pic_path='/home/kevin/project/dobot-project/opencv/MVS-picture.jpg', show_key=1)
    t = []
    for i in pixel_coordinates:
        dobot_list = cv_to_dobot(cv_list=i, M=M)
        t.append(dobot_list)
    while True:
        os.system('clear')
        print(t)
        print(a_list)
        print("input 0 to exit")
        print(device.pose())
        x = int(input("please input x:"))
        if x == 0:
            break
        y = int(input("please input y:"))
        if y == 0:
            break
        z = int(input("please input z:"))
        if z == 0:
            break
        r = int(input("please input r:"))
        if r == 0:
            break
        device.move_to(x,y,z,r,wait=True)
        input("press any key to continue......")

            

