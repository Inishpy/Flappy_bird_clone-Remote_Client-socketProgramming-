import socket

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MSG = '!Disconnect'
#SERVER = "192.168.8.100"
SERVER = socket.gethostbyname(socket.gethostname()) #THIS wont work if server is not in your pc then you
                                                    #have to type the address
ADDR = (SERVER, PORT)



Client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Client.connect(ADDR)


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))

    Client.send(send_length)
    Client.send(message)
    return Client.recv(2048).decode(FORMAT)    #reciving from server max byte size here is 2048  or anything


#send("Hello World! ")

#send("Hello Worl! ")

#send("Hello Wor! ")

#send(DISCONNECT_MSG)
