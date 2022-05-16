import os
import time












def menu1():
    os.system('clear')
    print("PC input control")
    print("+----------------------------------------------------------------------------------------")
    print("please input the num in [] to start dobot control                                       -")
    print("[1]:get new picture                                                                     -")
    print("[2]:get blue object blocks                                                              -")
    print("[3]:get red object blocks                                                               -")
    print("[4]:get green object blocks                                                             -")
    print("[5]:get yellow object blocks                                                            -")
    print("[6]:dobot back to home                                                                  -")
    print("[0]:back to the previous page                                                           -")
    print("[9]:debugging your dobot and picture coordinate                                         -") 
    print("+----------------------------------------------------------------------------------------")



def menu2():
    os.system('clear')
    print("please choose mode")
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("please input the num in [] to choose mode                      +")
    print("[1] PC input control                                           +")
    print("[2] voice control (under development..........)                +")
    print("[0] exit project                                               +")
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")


def menu0():
    os.system('clear')
    print("welcome to dobot control center!\n")
    print("++++++++++++++++++++++++++++++++++++++++\n")
    print("       *                               ")
    print("        *            ********          ")
    print("   ***********                         ")
    print("      *    *           ****            ")
    print("     *      *                          ")
    print("    *        *     *************       \n")
    print("++++++++++++++++++++++++++++++++++++++++")



def exit_menu():
    os.system('clear')
    print('thanks for using')
    print("++++++++++++++++++++++++++++++++++++++++\n")
    print("       *                               ")
    print("        *            ********          ")
    print("   ***********                         ")
    print("      *    *           ****            ")
    print("     *      *                          ")
    print("    *        *     *************       \n")
    print("++++++++++++++++++++++++++++++++++++++++")



def menu_voice():
    os.system('clear')
    print('welcome to voice control center')
    print("++++++++++++++++++++++++++++++++++++++++\n")
    print("       *                               ")
    print("        *            ********          ")
    print("   ***********                         ")
    print("      *    *           ****            ")
    print("     *      *                          ")
    print("    *        *     *************       \n")
    print("++++++++++++++++++++++++++++++++++++++++")
    time.sleep(2)


def menu_10():
    os.system('clear')
    print("voice control")
    print("+----------------------------------------------------------------------------------------")
    print("please say these words to control dobot                                                 -")
    print("蓝色                                                                                 ")
    print("红色                                                             ")
    print("绿色                                                               ")
    print("黄色                                                             ")
    print("回去                                                            ")
    print("退出                                                                 ")
    print("+----------------------------------------------------------------------------------------")
