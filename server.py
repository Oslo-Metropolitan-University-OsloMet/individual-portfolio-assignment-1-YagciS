# Socket is going to be used to create TCP Server, sys will be used to be able to fetch the information
# the user will write to launch the program, threading is going to be used to keep the server listen
# for new connections and handle message traffic.

# ----- Imports ------- #
import socket
import sys
import threading
# --------------------- #

# I am using the traceback-limit so the user doesn't get annoyed with warning messages that doesn't mean anything
# These warning messages is coming up because the user didn't add all the parameters needed to launch the server
sys.tracebacklimit = 0

# We are first going to check if the user has entered the required parameters or has used -h/--help command
# If user has used -h/--help the program will write out the "manual" with an example of the syntax
# If user has just typed "python server.py" it will come up as exception, where they get some help
# The serverIP and serverPort variable is being instantiated, so we can create the server
try:
    serverIP = sys.argv[1]
    if serverIP == ('-h' or '--help'):
        print('To start the server, you need to specify they ip and port.\n'
              'Below this message is an example of the syntax:\n'
              '*-----------------------------------------*\n'
              '      python server.py localhost 7979\n'
              '*-----------------------------------------*')
    serverPort = int(sys.argv[2])
except(IndexError, ValueError):
    print("serverIP and Port must be specified, use -h or --help for more info")


# We instantiate a socket by specifying (address family (IPv4), socket type (TCP)
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# We continue with connecting/assign an IP address and port number to our Client Socket
serverSocket.bind((serverIP, serverPort))

# Here I will print some info so the user know that the server is launched successfully
# And show them their IP and Port, so if they forget what they wrote, they can just scroll up
print(f'\nWelcome to the server!\n'
      f'Binding successful!\n'
      f'This is your IP: {serverIP}\n'
      f'This is your Port: {serverPort}\n')

# We set the serverSocket to listen for incoming connections and instantiate the socket
# as a passive socket that will be used to accept incoming connection requiests with accept()
# We could set listen(1) if we wish to limit the connection requests before we call accept.
# if it comes 2 connection before we can call accept(), one of the connections will be droped
serverSocket.listen()

# We create a list for clientSockets so we can keep track on who is connected tp the server
clientSockets = []
# We also set a nickname list, so we can see what these connections has as their nicknames
connectedClients_has_nickname = []

# We instantiate the bots aswell. Here I wanted to know availablebots names, busyBots names
# and the socket for the busy sockets, so we know which bot is connected to each socket
availableBots = ['Chad', 'Elsa', 'Peter', 'Jarvis']
busyBotsSocket = []
busyBots = []

# This is the main broadcast function, that deals with sending the traffic to the right places
# First block of code is that if a client sends a message, the message is going to be broadcasted
# to everyone, but the client that sent it. This also includes the bots
# The second block of is sending the message from client to the bots, I couldn't manage to get it work in
# first block, therefore it had to be there
# The last block is checking if a bot sent a message, the message is only going to be forwarded to the clients
# NOT the other bots, this is because else we would have to deal with that the bots talk to each other non-stop
def broadcast(message, sentClient):
    if sentClient in clientSockets:
        for client in (clientSockets and busyBotsSocket):
            if client is not sentClient:
                client.send(message)



    if sentClient in busyBotsSocket:
        for client in clientSockets:
            if client is not sentClient:
                client.send(message)


# A simple function that handles Messages, it will receive messages from the socekets,
# send it to broadcast function that will handle whom the message is going to be sent to
# if there is no message that is being received, we would assume the socket has disconnected
# Therefore we run a function that will safely disconnect the socket, so someone else can use that
# socket and nickname
def handleMessageTraffic(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message, client)
        except:
            socketDisconnected(client)
            break

# We disconnect the socket and free both the socket and nickname
# This is done by first getting the index of the socket in the list
# Then remove the socket matching the parameter, then we close that socket
# Lastly we find the nickname used by that socket and broadcast that the user left
# and free that nickname so others can use it
# For the bots, we need to add the nickname back to "available bots" so we can call them again
# if we wish to do so
def socketDisconnected(socket):
    if socket in busyBotsSocket:
        index = busyBotsSocket.index(socket)
        busyBotsSocket.remove(socket)
        socket.close()
        nickname = busyBots[index]
        broadcast(f'>>Bot {nickname} left the chat!'.encode, None)
        busyBots.remove(nickname)
        availableBots.append(nickname)
    else:
        index = clientSockets.index(socket)
        clientSockets.remove(socket)
        socket.close()
        nickname = connectedClients_has_nickname[index]
        broadcast(f'>>{nickname} left the chat!'.encode(), None)
        connectedClients_has_nickname.remove(nickname)

# This is a check to see if Socket's nickname is available
# First "message" the client sends is going to be the nickname, therefore
# we can receive and decode that message that contains the nickname
# We first check if the name is taken by any clients, then if it's taken by any busyBots
# If not, then we can add it as new nickname, and send a confirmation to the client that the
# nickname is accepted and registered
def isNameAvailable(clientSocket):
    while True:
        nickname = clientSocket.recv(1024).decode()
        isNameTakenClient = any(nickname in x for x in connectedClients_has_nickname)
        isNameTakenBot = any(nickname in x for x in busyBots)
        if isNameTakenClient == False and isNameTakenBot == False:
            clientSocket.send('New nickname'.encode())
            return nickname
        else:
            clientSocket.send('Choose a new nickname: '.encode())

# This function is used to receive new connections and handle them
def receive():
    while True:
        # We start with accepting new connections, to have some information where this connection came from
        # I included "address" that is going to be printed in the servers terminal
        clientSocket, address = serverSocket.accept()
        print(f'Connected with {str(address)}')

        # We run isNameAvailable function and save the nickname, so we can broadcast and add in lists
        nickname = isNameAvailable(clientSocket)

        # If nickname is in availableBots, we are going to set it as busy bot, and register its socket
        if nickname in availableBots:
            availableBots.remove(nickname)
            busyBots.append(nickname)
            busyBotsSocket.append(clientSocket)

            # Then we print what the nickname of the bot is in server's side, then broadcast to everyone that
            # bot has joined the chat
            print(f'Nickname of the bot is {nickname}\n')
            broadcast(f'>>{nickname} bot joined the chat!'.encode(), clientSocket)

            # Else, we can assume that they are real users, and connect them that way
        else:
            clientSockets.append(clientSocket)
            connectedClients_has_nickname.append(nickname)

            print(f'Nickname of the client is {nickname}!\n')
            broadcast(f'>>{nickname} joined the chat!\n'.encode(), clientSocket)
            clientSocket.send('Connected to the server!'.encode())

        # Thread is used to keep MessageTraffic active, so users always gets updated chat
        thread = threading.Thread(target=handleMessageTraffic, args=(clientSocket,))
        thread.start()


#Confirmation that the server is running and starting receive()
print(f'Server is listening for new connections...\n')
receive()
