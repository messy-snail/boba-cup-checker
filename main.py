# -*- coding: utf-8 -*-

import camera_manager
import color_finder
from _thread import *
import socket
import sys
import getopt
import copy
import cv2
from time import sleep

VERSION = '1.3'

HOST = '127.0.0.1'
PORT = 7777
VIZ = False
WRITE = False
DEBUG = False
DELAY_TIME = 1.5

THRESHOLD_VAL = 30
BIN_COUNTER = 200
OPEN_ITER = 2

LEFT = 0
RIGHT = 640
TOP = 0
BOT = 480

STOP_FLAG = False

thread_status = None
server_socket = None
to_client_socket = None
addr = None

cm  = camera_manager.camera_manager()
cf = color_finder.color_finder()

def response(data):
    #decode
    global DELAY_TIME
    global VIZ
    global WRITE
    global BIN_COUNTER
    global THRESHOLD_VAL
    global OPEN_ITER

    global LEFT
    global RIGHT
    global TOP
    global BOT

    global STOP_FLAG
    msg = data.decode()

    msg_list = msg.split(' ')
    print(msg_list[0])

    if msg_list[0]=='init':
        cf.reference =copy.deepcopy(cm.frame)
        cv2.imwrite('reference.png', cf.reference)
        print('save the reference')

    elif msg_list[0]=='stat':
        start_new_thread(thread_send,(1,))
        
        # sleep(DELAY_TIME)
        # to_client_socket.send(result.encode("utf-8"))
    elif msg_list[0]=='stop':
        STOP_FLAG = True
    elif msg_list[0]=='set':
        arg_num =0
        response_string = 'success'
        for idx in range(1, len(msg_list)):
            if msg_list[idx] == '-v' or msg_list[idx] == '--viz':
                try:
                    if msg_list[idx+1] == 'True':
                        VIZ = True
                        arg_num += 1
                    elif msg_list[idx+1] == 'False':
                        VIZ = False
                        arg_num += 1
                    else:
                        response_string = 'fail,viz'
                        to_client_socket.send(response_string.encode("utf-8"))
                        return
                except:
                    response_string = 'fail,viz'
                    to_client_socket.send(response_string.encode("utf-8"))
                    print(response_string)
                    return
            if msg_list[idx] == '-w' or msg_list[idx] == '--write':
                try:
                    if msg_list[idx+1] == 'True':
                        WRITE = True
                        arg_num += 1
                    elif msg_list[idx+1] == 'False':
                        WRITE = False
                        arg_num += 1
                    else:
                        response_string = 'fail,write'
                        to_client_socket.send(response_string.encode("utf-8"))
                        return
                except:
                    response_string = 'fail,write'
                    to_client_socket.send(response_string.encode("utf-8"))
                    print(response_string)
                    return
            if msg_list[idx] == '-d' or msg_list[idx] == '--delay':
                try:
                    if float(msg_list[idx+1])>0 and float(msg_list[idx+1])<5.0 :
                        DELAY_TIME = float(msg_list[idx+1])
                        arg_num += 1
                    else:
                        response_string = 'fail,delay'
                        to_client_socket.send(response_string.encode("utf-8"))
                        return
                except:
                    response_string = 'fail,delay'
                    to_client_socket.send(response_string.encode("utf-8"))
                    print(response_string)
                    return

            if msg_list[idx] == '-c' or msg_list[idx] == '--counter':
                try:
                    if int(msg_list[idx+1])>9 and int(msg_list[idx+1])<245761:
                        BIN_COUNTER = int(msg_list[idx+1])
                        arg_num += 1
                    else:
                        response_string = 'fail,counter'
                        to_client_socket.send(response_string.encode("utf-8"))
                        return
                except:
                    response_string = 'fail,counter'
                    to_client_socket.send(response_string.encode("utf-8"))
                    print(response_string)
                    return
            if msg_list[idx] == '-q' or msg_list[idx] == '--threshold':
                try:
                    if int(msg_list[idx+1])>0 and int(msg_list[idx+1])<255:
                        THRESHOLD_VAL = int(msg_list[idx+1])
                        arg_num += 1
                    else:
                        response_string = 'fail,threshold'
                        to_client_socket.send(response_string.encode("utf-8"))
                        return
                except:
                    response_string = 'fail,threshold'
                    to_client_socket.send(response_string.encode("utf-8"))
                    print(response_string)
                    return

            if msg_list[idx] == '-o' or msg_list[idx] == '--open':
                try:
                    if int(msg_list[idx+1])>0 and int(msg_list[idx+1])<6:
                        OPEN_ITER  = int(msg_list[idx+1])
                        arg_num += 1
                    else:
                        response_string = 'fail,open'
                        to_client_socket.send(response_string.encode("utf-8"))
                        return
                except:
                    response_string = 'fail,open'
                    to_client_socket.send(response_string.encode("utf-8"))
                    print(response_string)
                    return
            if msg_list[idx] == '-l' or msg_list[idx] == '--left':
                try:
                    if int(msg_list[idx+1])>=0 and int(msg_list[idx+1])<640:
                        LEFT  = int(msg_list[idx+1])
                        arg_num += 1
                    else:
                        response_string = 'fail,left'
                        to_client_socket.send(response_string.encode("utf-8"))
                        return
                except:
                    response_string = 'fail,left'
                    to_client_socket.send(response_string.encode("utf-8"))
                    print(response_string)
                    return    
            if msg_list[idx] == '-r' or msg_list[idx] == '--right':
                try:
                    if int(msg_list[idx+1])>=0 and int(msg_list[idx+1])<640:
                        RIGHT  = int(msg_list[idx+1])
                        arg_num += 1
                    else:
                        response_string = 'fail,right'
                        to_client_socket.send(response_string.encode("utf-8"))
                        return
                except:
                    response_string = 'fail,right'
                    to_client_socket.send(response_string.encode("utf-8"))
                    print(response_string)
                    return
            if msg_list[idx] == '-t' or msg_list[idx] == '--top':
                try:
                    if int(msg_list[idx+1])>=0 and int(msg_list[idx+1])<480:
                        TOP  = int(msg_list[idx+1])
                        arg_num += 1
                    else:
                        response_string = 'fail,top'
                        to_client_socket.send(response_string.encode("utf-8"))
                        return
                except:
                    response_string = 'fail,top'
                    to_client_socket.send(response_string.encode("utf-8"))
                    print(response_string)
                    return
            if msg_list[idx] == '-b' or msg_list[idx] == '--bot':
                try:
                    if int(msg_list[idx+1])>=0 and int(msg_list[idx+1])<480:
                        BOT  = int(msg_list[idx+1])
                        arg_num += 1
                    else:
                        response_string = 'fail,bot'
                        to_client_socket.send(response_string.encode("utf-8"))
                        return
                except:
                    response_string = 'fail,bot'
                    to_client_socket.send(response_string.encode("utf-8"))
                    print(response_string)
                    return                    

        if (len(msg_list)-1) == arg_num*2:
            response_string = 'success'
        else:
            response_string = 'fail,args'

        cm.viz = VIZ
        cm.write = WRITE
        cf.viz = VIZ
        cf.write = WRITE
        cf.threshold_val = THRESHOLD_VAL
        cf.bin_counter = BIN_COUNTER
        cf.open_iteration = OPEN_ITER

        to_client_socket.send(response_string.encode("utf-8"))
        print(response_string)

def thread_server(id):
    global server_socket
    global thread_status
    global to_client_socket
    global addr

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind((HOST, PORT))


    thread_status = 1

    print('start socket')
    while True:
        if thread_status ==1:

            server_socket.listen()
            to_client_socket, addr = server_socket.accept()
            thread_status = 2
            con_msg = '[??????] {}:{}'.format(addr[0], addr[1])
            print(con_msg)
        elif thread_status==2:

            try:
                # ???????????? ???????????? ?????????????????? ?????? ???????????????.(??????)
                data = to_client_socket.recv(1024)
                print(data)
                if data:
                    msg = '[??????] {0}:{1} / {2}'.format(addr[0], addr[1], data.decode())
                    print(msg)

                if not data:
                    thread_status = 1
                    to_client_socket.close()
                    continue

                # ???????????? ????????? ??????
                response(data)

            except ConnectionResetError as e:
                exception_msg = '[??????] {}:{}'.format(addr[0], addr[1])
                print(exception_msg)
                break
    print('socket bye')
           
def thread_send(id):
    global STOP_FLAG
    global to_client_socket
    while True:
        result = cf.is_cup(cm.frame)
        print(result)
        to_client_socket.send(result.encode("utf-8"))
        if STOP_FLAG == True:
            STOP_FLAG = False
            break

    # while STOP_FLAG==False:
    #     to_client_socket.send(result.encode("utf-8"))

def main(argv):
    FILE_NAME     = argv[0] # command line arguments??? ???????????? ?????????
    global HOST
    global PORT
    global VIZ
    global WRITE
    global DELAY_TIME
    global BIN_COUNTER
    global THRESHOLD_VAL
    global OPEN_ITER
    global LEFT
    global RIGHT
    global TOP
    global BOT
    try:
        # opts: getopt ????????? ?????? ?????? ex) [('-i', 'myinstancce1')]
        # etc_args: getopt ?????? ????????? ????????? ?????? Argument
        # argv ?????????(index:0)??? ?????????, ?????????(index:1)?????? Arguments
        opts, etc_args = getopt.getopt(argv[1:], \
                                 "hi:p:v:w:d:c:q:o:l:r:t:b:", ["help","ip=","port=","viz=","write=","delay=",
                                 "counter=","threshold=","open=",
                                 "left=","right=","top=","bot="])

    except getopt.GetoptError: # ??????????????? ???????????? ?????? ??????
        print(FILE_NAME, '-i <ip> -p <port>, -v <viz> -w <write> -d <delay> -c <bin counter> -q <threshold value> -o <open iteration> -l <left> -r <right> -t <top> -b <bot>')
        sys.exit(2)

    for opt, arg in opts: # ????????? ????????? ??????
        if opt in ("-h", "--help"): # HELP ????????? ?????? ????????? ??????
            print(FILE_NAME, '-i <ip> -p <port>, -v <viz> -w <write> -d <delay> -c <bin counter> -q <threshold value> -o <open iteration> -l <left> -r <right> -t <top> -b <bot>')
            print('???????????? ????????? ??????')
            # print(f'ip={HOST}, port={PORT}, viz={VIZ}, write={WRITE}, delay time={DELAY_TIME}')
            print('ip={}, port={}, viz={}, write={}, delay time={}').format(HOST, PORT, VIZ, WRITE, DELAY_TIME)
            print('bin counter={}, threshold value={}, open iteration={}').format(BIN_COUNTER,THRESHOLD_VAL, OPEN_ITER)
            print('left={}, right={}, top={}, bot={}').format(LEFT, RIGHT, TOP, BOT)
            sys.exit()

        elif opt in ("-i", "--ip"): # IP ????????? ??????
            HOST = arg
        elif opt in ("-p", "--port"): # PORT ????????? ??????
            PORT = arg
        elif opt in ("-v", "--viz"): # VIZ ????????? ??????
            if arg == 'True':
                VIZ = True
            elif arg=='False':
                VIZ = False
            else:
                print('True ?????? False??? ???????????????. True or False')
                sys.exit()
        elif opt in ("-w", "--write"):  # WRITE ????????? ??????
            if arg == 'True':
                WRITE = True
            elif arg=='False':
                WRITE = False
            else:
                print('True ?????? False??? ???????????????. True or False')
                sys.exit()
        elif opt in ("-d", "--delay"): # DELAY_TIME ????????? ??????
            if float(arg)>0 and float(arg)<5.0:
                DELAY_TIME = float(arg)
            else:
                print('?????? ????????? ???????????????(0 ~ 5.0). Valid range(0 ~ 5.0) | Unit: Sec')
                sys.exit()
        elif opt in ("-c", "--counter"): # BIN_COUNTER ????????? ??????
            if int(arg)>9 and int(arg)<245761:
                BIN_COUNTER = int(arg)
            else:
                print('?????? ????????? ???????????????(10 ~ 245,760). Valid range(10 ~ 245,760)')
                sys.exit()
        elif opt in ("-t", "--threshold"): # THRESHOLD_VAL ????????? ??????
            if int(arg)>0 and int(arg)<255:
                THRESHOLD_VAL = int(arg)
            else:
                print('?????? ????????? ???????????????(1 ~ 254). Valid range(1 ~ 254)')
                sys.exit()

        elif opt in ("-o", "--open"): # OPEN_ITER ????????? ??????
            if int(arg)>0 and int(arg)<6:
                OPEN_ITER = int(arg)
            else:
                print('?????? ????????? ???????????????(0 ~ 5). Valid range(0 ~ 5)')
                sys.exit()
        elif opt in ("-l", "--left"): # LEFT ????????? ??????
            if int(arg)>=0 and int(arg)<640:
                LEFT = int(arg)
            else:
                print('?????? ????????? ???????????????(0~640). Valid range(0 ~ 640)')
                sys.exit()       
        elif opt in ("-r", "--right"): # RIGHT ????????? ??????
            if int(arg)>=0 and int(arg)<640:
                RIGHT = int(arg)
            else:
                print('?????? ????????? ???????????????(0~640). Valid range(0 ~ 640)')
                sys.exit()    
        elif opt in ("-t", "--top"): # TOP ????????? ??????
            if int(arg)>=0 and int(arg)<480:
                TOP = int(arg)
            else:
                print('?????? ????????? ???????????????(0~480). Valid range(0 ~ 480)')
                sys.exit()     
        elif opt in ("-b", "--bot"): # BOT ????????? ??????
            if int(arg)>=0 and int(arg)<480:
                BOT = int(arg)
            else:
                print('?????? ????????? ???????????????(0~480). Valid range(0 ~ 480)')
                sys.exit()                                                         

    cm.viz = VIZ
    cm.write = WRITE
    cf.viz = VIZ
    cf.write = WRITE
    cf.threshold_val = THRESHOLD_VAL
    cf.bin_counter = BIN_COUNTER
    cf.open_iteration = OPEN_ITER

    cm.left = LEFT
    cm.right = RIGHT
    cm.top = TOP
    cm.bot = BOT

    print("IP:", HOST)
    print("PORT:",  PORT)
    print('==================')
    print("DELAY_TIME:", DELAY_TIME)
    print("THRESHOLD_VAL:", THRESHOLD_VAL)
    print("BIN_COUNTER:", BIN_COUNTER)
    print("OPEN_ITER:", OPEN_ITER)



# module??? ?????? main?????? ????????? ?????? ????????????
if __name__ == "__main__":
    print('Version:', VERSION)
    main(sys.argv)

    start_new_thread(thread_server,(0,))

    if cm.Open()==False:
        print('check cam')
    if cm.Run() == False:
        print('check cam')
    else:
        print('good bye')
    sys.exit()

