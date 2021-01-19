import socket
import threading

# Choosing a nickname
nickname = input("Enter a nickname: ")

# Connecting the client to the server
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((socket.gethostbyname(socket.gethostname()), 12458))

# Listening to the server and Sending the nickname
def receive():
    while True:
        try:
            # Receive a message from the server (Not visible to user)
            message = clientSocket.recv(1024).decode('ascii')

            if message == 'NICK':
                clientSocket.send(nickname.encode('ascii'))
            else:
                print('>' + message)
        except:
            # Close the connection if an error occurs
            print('An error occured')
            clientSocket.close()
            break

# A function which helps in writing messages
def write():
    while True:
        message = '> {}: {}'.format(nickname, input(' '))
        clientSocket.send(message.encode('ascii'))

# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
