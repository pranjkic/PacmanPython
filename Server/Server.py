import socket
import threading

HOST = ''       # Symbolic name meaning all available interfaces
PORT = 50005    # Arbitrary non-privileged port
conn1 = 0
conn2 = 0


def firstSocket():
    text1 = ''
    while True:
        bin = conn1.recv(5)
        text1 += str(bin, 'utf8')
        if bin:
            conn2.sendall(text1.encode('utf8'))
            text1 = ''


def secondSocket():
    text2 = ''
    while True:
        bin = conn2.recv(5)
        text2 += str(bin, 'utf8')
        if bin:
            conn1.sendall(text2.encode('utf8'))
            text2 = ''


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(2)

    conn1, addr1 = s.accept()
    print('Connected by', addr1)
    conn1.sendall("1".encode('utf8'))
    conn2, addr2 = s.accept()
    print('Connected by', addr2)
    conn2.sendall("2".encode('utf8'))

    conn1.sendall("start".encode('utf8'))
    conn2.sendall("start".encode('utf8'))

    '''with conn1 and conn2:'''
    if conn1 != 0 and conn2 != 0:
        th1 = threading.Thread(target=firstSocket, args=(), daemon=False)
        th1.start()

        th2 = threading.Thread(target=secondSocket, args=(), daemon=False)
        th2.start()




