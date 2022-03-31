# ----- Imports ------- #
import socket
import sys
import threading
import bot
# We import bot.py as bot to be able to control what the bots are going to respond
# --------------------- #

# First I am going to check if the user has entered the required parameters or has used -h/--help command
# If user has used -h/--help the program will write out the "manual" with an example of the syntax
# I also specify serverIP and serverPort variable that is going to be used to connect the client to the server
try:
    serverIP = sys.argv[1]
    if serverIP == ('-h' or '--help'):
        print('Before you start client.py, make sure server.py is running'
              'To start the client, you need to specify server\'s ip and port.\n'
              'In addition, you need to add the nickname of the client'
              'Below this message is an example of the syntax:\n'
              '*-----------------------------------------*\n'
              '   python client.py localhost 7979 name\n'
              '*-----------------------------------------*')
    serverPort = int(sys.argv[2])
except(IndexError, ValueError):
    print("serverIP and Port must be specified, use -h or --help for more info")

# First we instantiate a socket by specifying (address family (IPv4), socket type (TCP)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# We continue with connecting/assign an IP address and port number to our Client Socket
client.bind((serverIP, serverPort))

# We instantiate the socketNickname with the parameter given by the user
socketNickname = sys.argv[3]

# Instantiating the botNames, so if used, we know that these are bots and is going to behave like a bot
botNames = ['Chad', 'Elsa', 'Peter', 'Jarvis']

# Checking if the socketNickname is available by sending socketNickname to server
# If socketNickname is not available, the user will be asked to enter new socketNickname
# If socketNickname is in botNames, the bot terminal will get a message that the Bot is active
while True:
    client.send(socketNickname.encode())
    message = client.recv(1024).decode()
    if message == "Choose a new nickname: ":
        socketNickname = input(f'{message}')
    else:
        if socketNickname in botNames:
            print(f'Bot {socketNickname} is now activated')
        break


# If user is a bot, then we want to forward the message written by Client
# This message is first decoded, then returned to the server after going through bot.py
# Else, the user must be a Client, the message is decoded and shown in their terminal
# A little exception if there happens a timeout in the server. This will close all
# clients and end the program
def receive():
    while True:
        try:
            if socketNickname in botNames:
                message = client.recv(1024).decode()
                message = bot.botResponse(message, socketNickname)
                client.send(message.encode())
            else:
                message = client.recv(1024).decode()
                print(f'{message}')
        except:
            print("An error occurred!")
            client.close()
            break


# If user is a bot, they will not be able to write stuff directly in the terminal
# else, the client (real user) will be able to communicate here
def write():
    if socketNickname not in botNames:
        while True:
            message = f'{socketNickname}: {input("")}'
            client.send(message.encode())


# Thread is used to keep both receive() and write() active, so the user will
# be able to interact with the program instantly
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
