import camera_manager 
import color_finder as cf
from _thread import *
import socket
import sys
import getopt


HOST = '127.0.0.1'
PORT = 7777
VIZ = True
WRITE = False

thread_status = None
server_socket = None
to_client_socket = None
addr = None

cm  = camera_manager.camera_manager()

def response(data):
        # 메시지 복호
        msg = data.decode()

        msg_list = msg.split(':')
        print(msg_list[0])

        # 수신 받은 데이터 포즈 정보일 때 처리
        if msg=='iscup':
            result = cf.is_cup(cm.frame, VIZ, WRITE)
            print(result)
            to_client_socket.send(result.encode("utf-8"))

def thread_server(id):
    print('start')
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
            con_msg = f'[연결] {addr[0]}:{addr[1]}'
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
                exception_msg = f'[끊김] {addr[0]}:{addr[1]}'
                print(exception_msg)
                break
    print('socket bye')
           
def main(argv):
    FILE_NAME     = argv[0] # command line arguments의 첫번째는 파일명
    global HOST
    global PORT
    global VIZ
    global WRITE
    try:
        # opts: getopt 옵션에 따라 파싱 ex) [('-i', 'myinstancce1')]
        # etc_args: getopt 옵션 이외에 입력된 일반 Argument
        # argv 첫번째(index:0)는 파일명, 두번째(index:1)부터 Arguments
        opts, etc_args = getopt.getopt(argv[1:], \
                                 "hi:p:v:w:", ["help","ip=","port=","viz=","write="])

    except getopt.GetoptError: # 옵션지정이 올바르지 않은 경우
        print(FILE_NAME, '-i <ip> -p <port> -v <viz> -w <write>')
        sys.exit(2)

    for opt, arg in opts: # 옵션이 파싱된 경우
        if opt in ("-h", "--help"): # HELP 요청인 경우 사용법 출력
            print(FILE_NAME, '-i <ip address> -p <port>, -v <viz> -w <write>')
            sys.exit()

        elif opt in ("-i", "--ip"): # IP 입력인 경우
            HOST = arg
        elif opt in ("-p", "--port"): # PORT 입력인 경우
            PORT = arg
        elif opt in ("-v", "--viz"): # VIZ 입력인 경우
            if arg == 'True' or arg == 'False':
                VIZ = arg
            else:
                print('True or False')
                sys.exit()
        elif opt in ("-w", "--write"):  # WRITE 입력인 경우
            if arg=='True' or arg=='False':
                WRITE = arg
            else:
                print('True or False')
                sys.exit()

    # if len(INSTANCE_NAME) < 1: # 필수항목 값이 비어있다면
    #     print(FILE_NAME, "-i option is mandatory") # 필수임을 출력
    #     sys.exit(2)

    print("IP:", HOST)
    print("PORT:",  PORT)



# module이 아닌 main으로 실행된 경우 실행된다
if __name__ == "__main__":
    main(sys.argv)
    start_new_thread(thread_server,(0,))
    # thread_server(0)
    print('test')
    
    cm.Open()

    cm.Run(VIZ, WRITE)

