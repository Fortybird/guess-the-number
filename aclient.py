import socket

# Admin socket
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
TCP_IP = "127.0.0.1"
TCP_PORT= 4001



# Admin protocol
def admin():
        s.connect((TCP_IP, TCP_PORT))
        s.send("Hello\r\n".encode())
        admingreet = s.recv(80).decode()
        if admingreet == "Admin-Greetings\r\n":
                #print('Connected to:',"127.0.0.1,4001")
                s.send("Who\r\n".encode())             

# Listt to display of actice clients for Admin        
def ClientList():
    print("Online Clients at the moment:")
    while True:
        clients = s.recv(80).decode()
        if clients != "":
            clients = clients.rstrip()
            print(clients)
        else:
            break
    s.close()


admin()
ClientList()

    
