import socket
from math import pi

# HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
HOST = "192.168.8.101"  # Standard loopback interface address (localhost)
#HOST = socket.gethostname()
print(HOST)
# PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
PORT = 12345  # Port to listen on (non-privileged ports are > 1023)
go_thread = True
moveL = False
moveR = False

def listeningGuest():
    print('in listeningGuest')
    global moveL, moveR
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print('socket')
        s.bind((HOST, PORT))
        print('after bind')
        s.listen()
        print('after listen')
        s.settimeout(2.0) # is added to avoid situation when while loop is waiting for response from client. Loop will be resetting every 2.0 sec
        
        while go_thread:
            print('in the loop')
            try:
                conn, addr = s.accept()
                print('after accept')
                with conn:
                    print(f"Connected by {addr}")
                    #while True:
                    data = conn.recv(8)
                    print(data)
                    data = int.from_bytes(data, 'big')
                    # print()
                    # data = data + str.encode(' filip ')
                    print(data)
                    if data == 1: moveL = True
                    if data == 2: moveR = True
                    # if not data:
                    #     break
                    #conn.sendall(b'Hello, raspberry')
            except:
                print('TIMEOUT')
        print('Thread terminates')
def stopThread():
    global go_thread
    go_thread = False
    print('in function')