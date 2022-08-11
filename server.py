from json import dumps
from queue import Empty
import socket
from math import pi
# import struct
from struct import pack, unpack

# HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
HOST = "192.168.8.101"  # Standard loopback interface address (localhost)
#HOST = socket.gethostname()
print(HOST)
# PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
PORT = 12345  # Port to listen on (non-privileged ports are > 1023)
go_thread = True
moveL = False
moveR = False
step = [0, 0]
k = 0
paintX = 0
paintY = 0

class gamehost():
    def __init__(self):
        self.step = [0, 0]

def listeningGuest():
    print('in listeningGuest')
    global moveL, moveR
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        #print('socket')
        s.bind((HOST, PORT))
        #print('after bind')
        s.listen()
        #print('after listen')
        s.settimeout(2.0) # is added to avoid situation when while loop is waiting for response from client. Loop will be resetting every 2.0 sec
        
        while go_thread:
            try:
                conn, addr = s.accept()
                with conn:
                    #print(f"Connected by {addr}")
                    #while True:
                    data = conn.recv(2)
                    #print(data)
                    data = int.from_bytes(data, 'big')
                    # print()
                    # data = data + str.encode(' filip ')
                    #print(data)
                    if data == 1: moveL = True
                    if data == 2: moveR = True
                    # if not data:
                    #     break
                    #print(Ghost.step)
                    if Ghost.step is not Empty:
                        conn.sendall(Ghost.step)
            except:
                print('TIMEOUT')
        print('Thread terminates')
def stopThread():
    global go_thread
    go_thread = False
    print('in function')

def paintRoute(move: list)-> None:
    Ghost.step = 0
    temp = ''
    for i in range(len(move)):
        temp += str(move[i].playerx) + ' '
        temp += str(move[i].playery)
        if i+1 != len(move): temp += ' ' # avoid adding space in the last iteration
        # Ghost.step += bytes(str(move[i].playerx), 'utf-8')
        # Ghost.step += bytes(str(move[i].playerx), 'utf-8')
        # print(move[i].playerx)
        # print(move[i].playery)
        # print()
    #Ghost.step = bytes(str(move), 'utf-8')
    #print(temp)
    Ghost.step = bytes(temp, 'utf-8')

Ghost = gamehost()