import socket
import random
import threading
import re

# Setup Port(s) and IP 
TCP_IP = "127.0.0.1"
TCP_PORTP = 4000
TCP_PORTA = 4001
# Creating Client's socket
try:
    sp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sp.bind((TCP_IP,TCP_PORTP))
    sp.listen(5)
except socket.error:
    print("Failed to create socket with Client.")
# Creating Admin's socket
try:
    sa = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sa.bind((TCP_IP,TCP_PORTA))
    sa.listen(5)
except socket.error:
    print("Failed to create socket with Admin.")
# Server is ready to take active client connections 
# Thread "tc" to host online Clients
def ClientWaitlist():
    print("waiting for Client connection...")
    while True:
        clientlist = sp.accept()
        connp = clientlist[0]
        addrp = clientlist[1]
        print("Player connected from:",addrp)
        tc = threading.Thread(target = StartClient , args = clientlist)
        tc.start()

    
# Connect client to server Protocol       
def Client(conn, addr):        
    try:
        # Protocol messages
        hello = conn.recv(80).decode()
        if hello== "Hello\r\n":
            conn.send("Greetings\r\n".encode())            
        game = conn.recv(80).decode()
        if game == "Game\r\n":
            conn.send("Ready\r\n".encode())
    # If problem occurs        
    except:
        socks.remove(conn)
        conn.close()
# After succesfull connection of client
# Ready for more than one connections
# Random number generates to all available clients
def StartClient(connc,addrc):
    Client(connc,addrc)
    activeclient.append(addrc)
    global guess
    answer = random.randint(1, 30)
    print(answer)
    while guess != answer:
        runGame(connc, answer)
    activeclient.remove(addrc)
    
# Executing the gamae to every client connected        
def runGame(conn,answer):
    global guess
    # Guessing sequence for client
    guessed = False
    while not guessed:        
        try:
            message = conn.recv(80).decode()
        except:
            break
        split = message.split(" ")
        guess = int(split[3])        
        # Checks answer(s) given by client        
        proximity = abs(guess - answer)
        if proximity == 0:        
            conn.send("Correct\r\n".encode())
            guessed = True                
        elif proximity < 3:
            conn.send("Close\r\n".encode())                
        else:
            conn.send("Far\r\n".encode())
# Server setup and ready to take an Admin client
# Thread "ta" to host all available clients 
def Admin():
    print("waiting for Admin...")
    while True:
        adminList = sa.accept()
        conna = adminList[0]
        addra = adminList[1]
        print("Admin connected from:", addra)
        ta = threading.Thread(target=startAdmin, args=adminList)
        ta.start()
    sa.close()
# Prepares the list of active clients for Admin
def listAdmin(conna,addra):
    for i in activeclient:
        strClient = str(str(i[0]) + " " + str(i[1]) + "\r\n")                        
        conna.send(strClient.encode())
    conna.close()
# Admin and Server protocol
def startAdmin(conna,addra):
    hello = conna.recv(80).decode()
    if hello == "Hello\r\n":
        conna.send("Admin-Greetings\r\n".encode())
    who = conna.recv(80).decode()
    if who == "Who\r\n":
        print("Admin Connected succesfully")
    listAdmin(conna, addra)
    
# When successfully connected
guess = 0
activeclient= []
# Thread for accepting all connections at the same time
# Lists for thread to take place
tclientWaitlist = threading.Thread(target = ClientWaitlist)
tclientWaitlist.start()
tadmin = threading.Thread(target = Admin)
tadmin.start()

