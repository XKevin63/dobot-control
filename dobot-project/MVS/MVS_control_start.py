import ctypes
from statistics import pstdev
import sys
import time
import numpy as np
import cv2
import termios
from pynput.keyboard import Key, Controller


sys.path.append('../MvImport')
from MvCameraControl_class import *



def press_any_key_exit():
    fd = sys.stdin.fileno()
    old_ttyinfo = termios.tcgetattr(fd)
    new_ttyinfo = old_ttyinfo[:]
    new_ttyinfo[3] &= ~termios.ICANON
    new_ttyinfo[3] &= ~termios.ECHO
    print(new_ttyinfo)
    # sys.stdout.write(msg)
    # sys.stdout.flush()
    termios.tcsetattr(fd, termios.TCSANOW, new_ttyinfo)
    try:
        os.read(fd, 7)
    except:
        pass
    finally:
        termios.tcsetattr(fd, termios.TCSANOW, old_ttyinfo)
        
    



# search alive device (USB3.0)
def device_search():

    device_list = MV_CC_DEVICE_INFO_LIST()
    ret = MvCamera.MV_CC_EnumDevices(nTLayerType=MV_USB_DEVICE, stDevList=device_list)
    
    if ret != 0:
        print('search device error,please check your code environment!')
        sys.exit()
    elif device_list.nDeviceNum == 0:
        print("find no alive device,please check your connect!")
        sys.exit()
    
    print('search complete!\n')
    print('find ', device_list.nDeviceNum, ' alive device\n')
    return device_list



# connect to device without log, device_num start from 0
def device_connect(device_list, device_num=0):

    if device_num + 1 > device_list.nDeviceNum:
        print('please input a appropriate number!')
        sys.exit()

    cam = MvCamera()
    device_choice = cast(device_list.pDeviceInfo[int(device_num)], POINTER(MV_CC_DEVICE_INFO)).contents
    
    ret = cam.MV_CC_CreateHandleWithoutLog(device_choice)
    
    if ret != 0:
        print('connect to ', device_num, ' device error,please check your code environment or your connect!')
        sys.exit()
    
    return cam, device_choice



# open your device
def device_open(cam):

    ret = cam.MV_CC_OpenDevice(MV_ACCESS_Exclusive, 0)
    if ret != 0:
        print('open device error,please check your connect!')
        sys.exit()
    




# 显示图像
def image_show(image):
    image = cv2.resize(image, (600, 400), interpolation=cv2.INTER_AREA)
    # cv2.imshow('fgmask', image)
    cv2.imwrite('/home/kevin/project/dobot-project/opencv/MVS-picture.jpg', image)
    k = cv2.waitKey(1) & 0xff


    



# 需要显示的图像数据转换
def image_control(data , stFrameInfo):
    if stFrameInfo.enPixelType == 17301505:
        image = data.reshape((stFrameInfo.nHeight, stFrameInfo.nWidth))
        image_show(image=image)
    elif stFrameInfo.enPixelType == 17301514:
        data = data.reshape(stFrameInfo.nHeight, stFrameInfo.nWidth, -1)
        image = cv2.cvtColor(data, cv2.COLOR_BAYER_GB2RGB)
        image_show(image=image)
    elif stFrameInfo.enPixelType == 35127316:
        data = data.reshape(stFrameInfo.nHeight, stFrameInfo.nWidth, -1)
        image = cv2.cvtColor(data, cv2.COLOR_RGB2BGR)
        image_show(image=image)
    elif stFrameInfo.enPixelType == 34603039:
        data = data.reshape(stFrameInfo.nHeight, stFrameInfo.nWidth, -1)
        image = cv2.cvtColor(data, cv2.COLOR_YUV2BGR_Y422)
        image_show(image = image)



winfun_ctype = CFUNCTYPE
stFrameInfo = POINTER(MV_FRAME_OUT_INFO_EX)
pData = POINTER(c_ubyte)
FrameInfoCallBack = winfun_ctype(None, pData, stFrameInfo, c_void_p)

def image_callback(pData, pFrameInfo, pUser):
    global img_buff
    img_buff = None
    stFrameInfo = cast(pFrameInfo, POINTER(MV_FRAME_OUT_INFO_EX)).contents

    if stFrameInfo:
        print(img_buff)
        print(stFrameInfo.enPixelType)
        print ("get one frame: Width[%d], Height[%d], nFrameNum[%d]" % (stFrameInfo.nWidth, stFrameInfo.nHeight, stFrameInfo.nFrameNum))

    if img_buff is None and stFrameInfo.enPixelType == 17301505:
        img_buff = (c_ubyte * stFrameInfo.nWidth*stFrameInfo.nHeight)()
        cdll.msvcrt.memcpy(byref(img_buff) , pData , stFrameInfo.nWidth*stFrameInfo.nHeight)
        data = np.frombuffer(img_buff , count = int(stFrameInfo.nWidth*stFrameInfo.nHeight) , dtype = np.uint8)
        image_control(data=data, stFrameInfo=stFrameInfo)
        del img_buff

    elif img_buff is None and stFrameInfo.enPixelType == 17301514:
        img_buff = (c_ubyte * stFrameInfo.nWidth*stFrameInfo.nHeight)()
        memmove(byref(img_buff) , pData , stFrameInfo.nWidth*stFrameInfo.nHeight)
        data = np.frombuffer(img_buff , count = int(stFrameInfo.nWidth*stFrameInfo.nHeight) , dtype = np.uint8)
        image_control(data=data, stFrameInfo=stFrameInfo)
        del img_buff  

    elif img_buff is None and stFrameInfo.enPixelType == 35127316:
        img_buff = (c_ubyte * stFrameInfo.nWidth * stFrameInfo.nHeight*3)()
        memmove(byref(img_buff), pData, stFrameInfo.nWidth * stFrameInfo.nHeight*3)
        data = np.frombuffer(img_buff, count=int(stFrameInfo.nWidth * stFrameInfo.nHeight*3), dtype=np.uint8)
        image_control(data=data, stFrameInfo=stFrameInfo)
        del img_buff 
        

    elif img_buff is None and stFrameInfo.enPixelType == 34603039:
        img_buff = (c_ubyte * stFrameInfo.nWidth * stFrameInfo.nHeight * 2)()
        cdll.msvcrt.memcpy(byref(img_buff), pData, stFrameInfo.nWidth * stFrameInfo.nHeight * 2)
        data = np.frombuffer(img_buff, count=int(stFrameInfo.nWidth * stFrameInfo.nHeight * 2), dtype=np.uint8)
        image_control(data=data, stFrameInfo=stFrameInfo)
        del img_buff 
CALL_BACK_FUN = FrameInfoCallBack(image_callback)



def set_off(cam):
    ret = cam.MV_CC_SetEnumValue("TriggerMode", MV_TRIGGER_MODE_OFF)
    if ret != 0:
        print ("set trigger mode fail!")
        sys.exit()



def image_catch(cam):
    ret = cam.MV_CC_RegisterImageCallBackEx(CALL_BACK_FUN, None)
    if ret != 0:
        print('register image callback fail!')
        sys.exit()
    
    ret = cam.MV_CC_StartGrabbing()
    if ret != 0:
        print("start grabbing fail!")
        sys.exit()

    # put # infront of next 2 code to get only one picture
    # print("press a key to stop grabbing.")
    # press_any_key_exit()
    time.sleep(0.1)
    

    ret = cam.MV_CC_StopGrabbing()
    if ret != 0:
        print ("stop grabbing fail!")
        sys.exit()
    

def cam_del(cam):
    ret = cam.MV_CC_CloseDevice()
    if ret != 0:
        print ("close deivce fail!")
        sys.exit()

    ret = cam.MV_CC_DestroyHandle()
    if ret != 0:
        print ("destroy handle fail!")
        sys.exit()



if __name__ == "__main__":
    device_list = device_search()
    cam, device_choice = device_connect(device_list=device_list, device_num=0)
    device_open(cam=cam)
    set_off(cam=cam)
    image_catch(cam=cam)
    cam_del(cam=cam)
    








