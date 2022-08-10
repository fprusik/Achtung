import socket

# HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
HOST = "192.168.8.101"  # Standard loopback interface address (localhost)
#HOST = socket.gethostname()
print(HOST)
# PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
PORT = 12345  # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    #print(s.listen())
    
    while True:
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            #while True:
            data = conn.recv(1024)
            print(data)
            data = int.from_bytes(data, 'big')
            # print()
            # data = data + str.encode(' filip ')
            print(data)
            # if not data:
            #     break
            conn.sendall(b'Hello, raspberry')
            