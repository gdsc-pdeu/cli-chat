import socket
import threading

host = socket.gethostbyname(socket.gethostname())
port = 12458

# Starting the Server
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((host, port))
serverSocket.listen()

# List for clients and their nicknames
clients = []
nicknames = []

# We want to broadcast the message to all the clients connected on the Server
def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            # As long as a message is received, we broadcast the message
            message = client.recv(1024)
            broadcast(message)
        except:
            # Cutting the connection to this client and removing it from the list
            index = clients.index(client)
            clients.remove(index)
            client.close()

            # Also remove the client's nickname and broadcast that the client left
            nickname = nicknames[index]
            broadcast(f'{nickname} has left the chat.'.encode('ascii'))
            nicknames.remove(nickname)

            break

def receive():
    while True:
        # Accepting the client connection
        client, address = serverSocket.accept()
        print(f"Connected with {str(address)}")

        # Requesting for a nickname from the client
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        # Broadcasting the message to all the clients in the server
        print(f'Nickname of the client is {nickname}')
        broadcast(f'{nickname} joined the chat.'.encode('ascii'))
        client.send('Connected to the server'.encode('ascii'))

        # Creating thread for handling the client
        # target is a callable object to be invoked
        thread = threading.Thread(target = handle, args = (client,))
        thread.start()  # Used to start a thread's activity
        # Printing the number of active connections apart from the main thread
        print(f"Active Connections: {threading.activeCount() - 1}")

print("The Server is listening.")
receive()
