import socket
import threading

#constants are given all caps
HEADER = 64
PORT = 5050
#SERVER = "192.168.8.100"
SERVER = socket.gethostbyname(socket.gethostname()) #same as above gethostname gives name of my device 
                                                       #and get hostbyname gives ip
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MSG = '!Disconnect'


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR) #bind this socket to this address so anything that connnets to the address now will hit this socket


message_ = 0
def handle_client(conn, addr):
    global message_
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)  #again this is waiting it blocks the running of code hence thread
                                                        #HEADER specifiy how many bytes to receive in first message 
                                                        #and the fact is this first message sends a number as to how many
                                                        #bytes its original next message is going to be 
                                                        #the message is encoded in utf-8 format so decoding in the same
        if msg_length:
            
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)        #this is the original message reception
            if msg == DISCONNECT_MSG:
                connected = False

            elif msg == "Hop!":
                message_ = 'Hop!'

            

            print(f"[{addr}] {msg}")
            conn.send("Message received!".encode(FORMAT))

    conn.close()                                     #this is import so that there is no error when the client 
                                                    #tries to connect next time


def start():
    server.listen()
    print(f"[LISTENING] Server is listening {SERVER}")
    while True:
        conn, addr = server.accept() #we need thread here because this code is blocking lines of code that is 
                                    #it waits for new connections so if we are creating threads to handle new connection 
                                    #then main thread can sit there and wait
                                    #conn is object of the client ie we can handle client by this object
                                    #addr is ip address and port of the new client
        thread = threading.Thread(target=handle_client, args=(conn, addr)) # this arguments are one which received by server accept
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")  # -1 one since 1 thread is the main thread already running



         

