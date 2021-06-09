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

VERSION = '1.0'

HOST = '127.0.0.1'
PORT = 7777
VIZ = False
WRITE = False
DEBUG = False
DELAY_TIME = 1.5

THRESHOLD_VAL = 30
BIN_COUNTER = 100
OPEN_ITER = 2

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
    msg = data.decode()

    msg_list = msg.split(' ')
    print(msg_list[0])

    if msg_list[0]=='init':
        cf.reference =copy.deepcopy(cm.frame)
        cv2.imwrite('reference.png', cf.reference)
        print('save the reference')

    elif msg_list[0]=='stat':
        while True:
            result = cf.is_cup(cm.frame)
            print(result)
            to_client_socket.send(result.encode("utf-8"))
            if result=='nocup':
                break
        # sleep(DELAY_TIME)
        # to_client_socket.send(result.encode("utf-8"))
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
            if msg_list[idx] == '-t' or msg_list[idx] == '--threshold':
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
            con_msg = '[연결] {}:{}'.format(addr[0], addr[1])
            print(con_msg)
        elif thread_status==2:

            try:
                # 데이터가 수신되면 클라이언트에 다시 전송합니다.(에코)
                data = to_client_socket.recv(1024)
                print(data)
                if data:
                    msg = '[수신] {0}:{1} / {2}'.format(addr[0], addr[1], data.decode())
                    print(msg)

                if not data:
                    thread_status = 1
                    to_client_socket.close()
                    continue

                # 컵있는지 없는지 확인
                response(data)

            except ConnectionResetError as e:
                exception_msg = '[끊김] {}:{}'.format(addr[0], addr[1])
                print(exception_msg)
                break
    print('socket bye')
           
def main(argv):
    FILE_NAME     = argv[0] # command line arguments의 첫번째는 파일명
    global HOST
    global PORT
    global VIZ
    global WRITE
    global DELAY_TIME
    global BIN_COUNTER
    global THRESHOLD_VAL
    global OPEN_ITER
    try:
        # opts: getopt 옵션에 따라 파싱 ex) [('-i', 'myinstancce1')]
        # etc_args: getopt 옵션 이외에 입력된 일반 Argument
        # argv 첫번째(index:0)는 파일명, 두번째(index:1)부터 Arguments
        opts, etc_args = getopt.getopt(argv[1:], \
                                 "hi:p:v:w:d:c:t:o:", ["help","ip=","port=","viz=","write=","delay=","counter=","threshold=","open="])

    except getopt.GetoptError: # 옵션지정이 올바르지 않은 경우
        print(FILE_NAME, '-i <ip> -p <port>, -v <viz> -w <write> -d <delay> -c <bin counter> -t <threshold value> -o <open iteration>')
        sys.exit(2)

    for opt, arg in opts: # 옵션이 파싱된 경우
        if opt in ("-h", "--help"): # HELP 요청인 경우 사용법 출력
            print(FILE_NAME, '-i <ip> -p <port>, -v <viz> -w <write> -d <delay> -c <bin counter> -t <threshold value> -o <open iteration>')
            print('설정값은 다음과 같다')
            # print(f'ip={HOST}, port={PORT}, viz={VIZ}, write={WRITE}, delay time={DELAY_TIME}')
            print('ip={}, port={}, viz={}, write={}, delay time={}').format(HOST, PORT, VIZ, WRITE, DELAY_TIME)
            print('bin counter={}, threshold value={}, open iteration={}').format(BIN_COUNTER,THRESHOLD_VAL, OPEN_ITER)
            sys.exit()

        elif opt in ("-i", "--ip"): # IP 입력인 경우
            HOST = arg
        elif opt in ("-p", "--port"): # PORT 입력인 경우
            PORT = arg
        elif opt in ("-v", "--viz"): # VIZ 입력인 경우
            if arg == 'True':
                VIZ = True
            elif arg=='False':
                VIZ = False
            else:
                print('True 또는 False를 입력하세요. True or False')
                sys.exit()
        elif opt in ("-w", "--write"):  # WRITE 입력인 경우
            if arg == 'True':
                WRITE = True
            elif arg=='False':
                WRITE = False
            else:
                print('True 또는 False를 입력하세요. True or False')
                sys.exit()
        elif opt in ("-d", "--delay"): # DELAY_TIME 입력인 경우
            if float(arg)>0 and float(arg)<5.0:
                DELAY_TIME = float(arg)
            else:
                print('적정 범위를 벗어납니다(0 ~ 5.0). Valid range(0 ~ 5.0) | Unit: Sec')
                sys.exit()
        elif opt in ("-c", "--counter"): # BIN_COUNTER 입력인 경우
            if int(arg)>9 and int(arg)<245761:
                BIN_COUNTER = int(arg)
            else:
                print('적정 범위를 벗어납니다(10 ~ 245,760). Valid range(10 ~ 245,760)')
                sys.exit()
        elif opt in ("-t", "--threshold"): # THRESHOLD_VAL 입력인 경우
            if int(arg)>0 and int(arg)<255:
                THRESHOLD_VAL = int(arg)
            else:
                print('적정 범위를 벗어납니다(1 ~ 254). Valid range(1 ~ 254)')
                sys.exit()

        elif opt in ("-o", "--open"): # OPEN_ITER 입력인 경우
            if int(arg)>0 and int(arg)<6:
                OPEN_ITER = int(arg)
            else:
                print('적정 범위를 벗어납니다(0 ~ 5). Valid range(0 ~ 5)')
                sys.exit()

    cm.viz = VIZ
    cm.write = WRITE
    cf.viz = VIZ
    cf.write = WRITE
    cf.threshold_val = THRESHOLD_VAL
    cf.bin_counter = BIN_COUNTER
    cf.open_iteration = OPEN_ITER

    print("IP:", HOST)
    print("PORT:",  PORT)
    print('==================')
    print("DELAY_TIME:", DELAY_TIME)
    print("THRESHOLD_VAL:", THRESHOLD_VAL)
    print("BIN_COUNTER:", BIN_COUNTER)
    print("OPEN_ITER:", OPEN_ITER)



# module이 아닌 main으로 실행된 경우 실행된다
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

