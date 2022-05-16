
from multiprocessing.connection import wait
import os
from sre_parse import Verbose
import sys
import numpy as np

from pydobot import Dobot
from serial.tools import list_ports






def device_connect(port_num=0):
    try:
        port = list_ports.comports()[port_num].device
        device = Dobot(port=port,verbose=False)
        device_home(device)
    except:
        print("connect dobot error,please check your connect!")
        sys.exit()
    
    return device


def device_home(device):
    (x,y,z,r,j1,j2,j3,j4) = (130, 0, 0, 1.5, -2.185, 4.5, 69, 3.9)
    try:
        device.move_to(x,y,z,r,wait=True)
        print('back home successful!')
    except:
        print("device back to home error,please check your connect!")



def cv_to_dobot(cv_list, M):
    dobot_list = []
    # dobot_list = np.dot(cv_list, M)[0]
    x = M[0][0]*cv_list[0]+M[0][1]*cv_list[1]+M[0][2]
    y = M[1][0]*cv_list[0]+M[1][1]*cv_list[1]+M[1][2]
    dx = x - 261 
    dy = y + 7
    print(dx)
    print(dy)
    if dx < -13 and dy > 12:
        dx = dx + 2
        dy = dy - 3
        print("C")
    # B
    if dx > 10 and dy < -15:
        dx = dx + 2
        dy = dy + 3
        print("B")
    if dx > 12 and dy > 13:
        dx = dx - 2
        dy = dy - 3
        print("A")
    # D
    if dx < -13 and dy < -13:
        dx = dx + 6
        dy = dy + 2
        print("D")
    w = dx
    dx = -dy
    dy = w
    x = dx + 261
    y = dy - 7
    dobot_list.append(x)
    dobot_list.append(y)

    return dobot_list




def device_location(device, mod=0):
    (x,y,z,r,j1,j2,j3,j4) = device.pose()
    if mod == 1:
        print("(x,y,z):(",x,",",y,",",z,")")
    elif mod == 2:
        print("(j1,j2,j3,j4):(",j1,",",j2,",",j3,",",j4,")")
    elif mod == 3:
        print("r:",r)
    elif mod == 0:
        print(f'x:{x} y:{y} z:{z} j1:{j1} j2:{j2} j3:{j3} j4:{j4}')



def device_jump(device, t_x, t_y, t_z, h_z=30):
    try:
        (x,y,z,r,j1,j2,j3,j4) = device.pose()
        device.move_to(x,y,h_z,r,wait=True)
        device.move_to(t_x,t_y,t_z,r,wait=True)
        # device.move_to(t_x,t_y,t_z,r,wait=True)
    except:
        print('error............')







# port = list_ports.comports()[0].device
# print(port)
# device = Dobot(port=port)
# (x,y,z,r,j1,j2,j3,j4) = device.pose()
# device.move_to(295,-45,-30,0,wait=True)
# device = device_connect(port_num=0)
# (x,y,z,r,j1,j2,j3,j4) = device.pose()
# print(f'x:{x} y:{y} z:{z} j1:{j1} j2:{j2} j3:{j3} j4:{j4}')
# device.move_to(x+1,y,z,r,wait=False)
# device.move_to(x+20,y,z,r,wait=False)

# device.close()
# port = list_ports.comports()[0].device
# device = Dobot(port=port,verbose=False)
# device_home(device)