import socket
from datetime import datetime

# Creating the socket(Internet,TCP)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect server to client protocol
def server():
    try:
        s.connect(("127.0.0.1", 4000))
        print("Connecting to:", "127.0.0.1, 4000\n")
        # If problem occurs
    except:
        print("Could not connect to server.")
    # Interoperability messages    
    try:
        s.send("Hello\r\n".encode())
        message = s.recv(80).decode()
        if message == "Greetings\r\n":            
            s.send("Game\r\n".encode())
            message = s.recv(80).decode()
        # If connection established , game starts
        if message == "Ready\r\n":
            name = input("What is your name: ")
            print("Welcome", name,"to the guess the number game!\n")
            
        running = 1

        while running!= 0:
            # Input of the client to guess a number
                while True:
                    try:
                        guess = int(input("Enter your guess: "))                    
                        break
                    #Input only integers
                    except ValueError:
                        print("Please enter a number!")
                # Format the guess, ready to send to the server
                guessstring = "My guess is: " + str(guess) + "\r\n"
                # Send the guess
                s.send(guessstring.encode())
                # Wait for the response from the server
                response = s.recv(80).decode()
                # Determine if the game is over
                if (response == "Correct\r\n"):
                    print("You guessed correctly!")
                    running = 0
                    print("Terminating connection...\nGame ended at:" + str(datetime.now()))                    
                    s.close()
                elif response == "Close\r\n":
                    print("You are close!")
                else:
                    print("You are way off!")
                    
        s.close()
    # If problem occurs from server    
    except:
        print("There are issues with the server. Connection has been terminated.\n")
        s.close()           
        
server()
