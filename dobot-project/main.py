
import os
import time


from opencv.opencv_color import eye_in_hand

from dobot.base_pydobot import *
from menu import *
from main_logic import *
from vioce_distinguish.voice_control import baidu_voice


dic_z = {'green':0, 'red':0, 'yellow':0, 'blue':0}


if __name__ == "__main__":

    menu0()
    input("press any key to initialization......")
    os.system('clear')
    M = eye_in_hand()
    print("initializate successfully!")
    time.sleep(1)

    while True:
        menu2()
        # print(M)
        try:
            mode_type = int(input("your choice:"))
        except:
            continue
        if mode_type == 0:
            exit_menu()
            time.sleep(2)
            os.system('clear')
            break
        elif mode_type != 1 and mode_type != 2:
            print("please input current number")
            time.sleep(2)
            continue
        
        os.system('clear')
        print("please waiting for connecting to dobot...........")
        # time.sleep(3)
        device = device_connect(port_num=0)
        print("connect to dobot successful")
        time.sleep(2)

        while mode_type == 1:
            menu1()
            try:
                control_type = int(input("your choice:"))
            except:
               continue
            if control_type == 1:
                os.system('clear')
                os.system('python3 /home/kevin/project/dobot-project/MVS/MVS_control_start.py')
                print("project done")
                input("enter any key to continue.........")

            elif control_type == 2:
                dic_z = sorting_block(clo='blue', device=device, M=M, dic_z=dic_z, show_key=1)

            elif control_type == 3:
                dic_z = sorting_block(clo='red', device=device, M=M, dic_z=dic_z, show_key=1)

            elif control_type == 4:
                dic_z = sorting_block(clo='green', device=device, M=M, dic_z=dic_z, show_key=1)

            elif control_type == 5:
                dic_z = sorting_block(clo='yellow', device=device, M=M, dic_z=dic_z, show_key=1)

            elif control_type == 6:
                os.system('clear')
                device_home(device=device)
                time.sleep(2)

            elif control_type == 7:
                while True:
                    dic_z = sorting_block(clo='blue', device=device, M=M, dic_z=dic_z, show_key=0)
                    dic_z = sorting_block(clo='green', device=device, M=M, dic_z=dic_z, show_key=0)
                    dic_z = sorting_block(clo='yellow', device=device, M=M, dic_z=dic_z, show_key=0)
                    os.system('python3 /home/kevin/project/dobot-project/MVS/MVS_control_start.py')
                    pixel_c1, a_l1 = color_location(color_type='blue', pic_path='/home/kevin/project/dobot-project/opencv/MVS-picture.jpg', show_key=0)
                    pixel_c2, a_l2 = color_location(color_type='green', pic_path='/home/kevin/project/dobot-project/opencv/MVS-picture.jpg', show_key=0)
                    pixel_c3, a_l3 = color_location(color_type='yellow', pic_path='/home/kevin/project/dobot-project/opencv/MVS-picture.jpg', show_key=0)
                    if len(pixel_c1) == 0 and len(pixel_c2) == 0 and len(pixel_c3) == 0:
                        break

            elif control_type == 0:
                device.close()
                break

            elif control_type == 9:
                debug_eye_to_hand(device=device, M=M)
            else:
                os.system('clear')
                print("please input current number")
                time.sleep(3)

            

        while mode_type == 2:
            menu_voice()
            while True:
                menu_10()
                input('press any key to start recording....')
                result_v = baidu_voice()
                if result_v["err_no"] != 0:
                    print('bad speech....')
                    print(result_v["err_msg"])
                    time.sleep(2)
                    continue
                elif result_v["result"] == ["蓝色"]:
                    dic_z = sorting_block(clo='blue', device=device, M=M, dic_z = dic_z)

                elif result_v["result"] == ["红色"]:
                    dic_z = sorting_block(clo='red', device=device, M=M, dic_z = dic_z)
                
                elif result_v["result"] == ["绿色"]:
                    dic_z = sorting_block(clo='green', device=device, M=M, dic_z = dic_z)

                elif result_v["result"] == ["黄色"]:
                    dic_z = sorting_block(clo='yellow', device=device, M=M, dic_z = dic_z)

                elif result_v["result"] == ["回去"]:
                    os.system('clear')
                    device_home(device=device)
                    time.sleep(2)

                elif result_v["result"] == ["退出"]:
                    device.close()
                    exit_menu()
                    time.sleep(2)
                    break

                else:
                    print("please say correct words...")
                    time.sleep(2)

                



            

    